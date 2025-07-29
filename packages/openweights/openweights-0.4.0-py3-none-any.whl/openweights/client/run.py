import asyncio
import atexit
import json
from typing import Optional, BinaryIO, Dict, Any, List, Union
import os
import sys
from postgrest.exceptions import APIError
import hashlib
from datetime import datetime
import backoff
from supabase import Client
import httpx
import logging
from functools import wraps


def is_transient_error(e):
    """Check if an error is likely transient and should be retried"""
    if isinstance(e, (httpx.RemoteProtocolError, httpx.ReadTimeout, httpx.ConnectTimeout)):
        return True
    return False

def retry_or_ignore(func, n_retries=5):
    """Retry a function, if it continues to fail, ignore the error"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        for i in range(n_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.error(f"Error in {func.__name__} (attempt {i+1}/{n_retries}): {e}")
                if i == n_retries - 1:
                    # On last attempt, return None instead of raising
                    return None
        return None
    return wrapper
    

class Run:
    def __init__(self, client: 'OpenWeights', job_id: Optional[str] = None, worker_id: Optional[str] = None, organization_id: Optional[str] = None, run_id: Optional[str] = None):
        self.client = client
        self._supabase = client._supabase
        self.organization_id = organization_id
        self.id = run_id or os.getenv('OPENWEIGHTS_RUN_ID')
        if self.id:
            # Run ID exists, fetch the data
            try:
                self._fetch_and_init_run(job_id, worker_id)
            except Exception as e:
                if not is_transient_error(e):
                    raise
                # For transient errors, retry with backoff
                self._fetch_and_init_run_with_retry(job_id, worker_id)
        else:
            # Create new run
            data = {
                'status': 'in_progress'
            }
            
            if job_id:
                data['job_id'] = job_id
            else:
                # Create a new script job
                command = ' '.join(sys.argv)
                job_data = {
                    'id': f"sjob-{hashlib.sha256(str(datetime.now().timestamp()).encode()).hexdigest()[:12]}",
                    'type': 'script',
                    'script': command,
                    'status': 'in_progress',
                    'organization_id': self.organization_id
                }
                job_result = self._supabase.table('jobs').insert(job_data).execute()
                data['job_id'] = job_result.data[0]['id']
            
            if worker_id:
                data['worker_id'] = worker_id

            # Get organization_id from job
            job = self._get_job_org_id_with_retry(data['job_id'])
            if not job.data:
                raise ValueError(f"Job {data['job_id']} not found")
            
            result = self._supabase.table('runs').insert(data).execute()
            self._load_data(result.data[0])

    @backoff.on_exception(
        backoff.expo,
        (httpx.RemoteProtocolError, httpx.ReadTimeout, httpx.ConnectTimeout),
        max_tries=5
    )
    def _fetch_and_init_run_with_retry(self, job_id, worker_id):
        """Fetch run data with retry logic"""
        self._fetch_and_init_run(job_id, worker_id)

    def _fetch_and_init_run(self, job_id, worker_id):
        """Fetch run data and initialize"""
        try:
            result = self._supabase.table('runs').select('*').eq('id', self.id).single().execute()
        except APIError as e:
            if 'contains 0 rows' in str(e):
                raise ValueError(f"Run with ID {self.id} not found")
            raise
        
        run_data = result.data
        if job_id and run_data['job_id'] != job_id:
            raise ValueError(f"Run {self.id} is associated with job {run_data['job_id']}, not {job_id}")
        
        if worker_id and run_data['worker_id'] != worker_id:
            # reassign run to self
            run_data['worker_id'] = worker_id
            result = self._supabase.table('runs').update(run_data).eq('id', self.id).execute()
            run_data = result.data[0]
        
        self._load_data(run_data)

    @backoff.on_exception(
        backoff.expo,
        (httpx.RemoteProtocolError, httpx.ReadTimeout, httpx.ConnectTimeout),
        max_tries=5
    )
    def _get_job_org_id_with_retry(self, job_id):
        """Get job organization ID with retry logic"""
        return self._supabase.table('jobs').select('organization_id').eq('id', job_id).single().execute()

    def _load_data(self, data: Dict[str, Any]):
        self.id = data['id']
        self.job_id = data['job_id']
        self.worker_id = data.get('worker_id')
        self.status = data['status']
        self.log_file = data.get('log_file')
        self.created_at = data['created_at']

    @staticmethod
    def get(supabase: Client, run_id: int) -> 'Run':
        """Get a run by ID"""
        run = Run(supabase)
        run.id = run_id
        try:
            result = supabase.table('runs').select('*').eq('id', run_id).single().execute()
        except APIError as e:
            if 'contains 0 rows' in str(e):
                raise ValueError(f"Run with ID {run_id} not found")
            raise
        run._load_data(result.data)
        return run

    @retry_or_ignore
    def update(self, status: Optional[str] = None, logfile: Optional[str] = None):
        """Update run status and/or logfile"""
        data = {}
        if status:
            data['status'] = status
        if logfile:
            data['log_file'] = logfile
        
        if data:
            result = self._supabase.table('runs').update(data).eq('id', self.id).execute()
            self._load_data(result.data[0])

    @retry_or_ignore
    def log(self, event_data: Dict[str, Any], file: Optional[BinaryIO] = None):
        """Log an event for this run"""
        if file:
            file_id = self._supabase.files.create(file, purpose='event')['id']
        else:
            file_id = None
        data = {
            'run_id': self.id,
            'data': event_data,
            'file': file_id
        }
        self._supabase.table('events').insert(data).execute()
    
    @property
    def events(self) -> List[Dict[str, Any]]:
        """Get all events for this run"""
        result = self._supabase.table('events').select('*').eq('run_id', self.id).execute()
        return result.data
    
    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)
    
    def download(self, target_dir):
        """Download artifacts for this run"""
        os.makedirs(target_dir, exist_ok=True)
        # Logs
        if self.log_file is not None:
            log = self.client.files.content(self.log_file)
            with open(f'{target_dir}/{self.id}.log', 'wb') as f:
                f.write(log)
        events = self.events
        for i, event in enumerate(events):
            if event['data'].get('file'):
                file = self.client.files.content(event['data']['file'])
                rel_path = event['data']["path"] if 'path' in event['data']  else event['data']['file']
                path = f'{target_dir}/{rel_path}'
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'wb') as f:
                    f.write(file)


class Runs:
    def __init__(self, client: 'OpenWeights'):
        self.client = client
        self._supabase = client._supabase
    
    @backoff.on_exception(backoff.constant, Exception, interval=1, max_time=60, max_tries=60, on_backoff=lambda details: print(f"Retrying... {details['exception']}"))
    def list(self, job_id: Optional[str] = None, worker_id: Optional[str] = None, limit: int = 10, status: Optional[str]=None) -> List[Dict[str, Any]]:
        """List runs by job_id or worker_id"""
        query = self._supabase.table('runs').select('*').limit(limit)
        if job_id:
            query = query.eq('job_id', job_id)
        if worker_id:
            query = query.eq('worker_id', worker_id)
        if status:
            query = query.eq('status', status)
        result = query.execute()
        return [Run(self.client, run_id=row['id']) for row in result.data]