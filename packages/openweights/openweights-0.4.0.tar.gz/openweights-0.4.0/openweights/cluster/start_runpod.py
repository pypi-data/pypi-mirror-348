"""
Usage:
    python start_runpod.py --gpu A6000 --container_disk_in_gb 25 --volume_in_gb 30

Note: possible unknown error with echo when running the script.
"""
import os
import time
import uuid

import backoff
import fire
import paramiko
import runpod
from dotenv import load_dotenv
from scp import SCPClient
from functools import lru_cache

load_dotenv(override=True) 

IMAGES = {
    'inference': 'nielsrolf/ow-inference-v2',
    'finetuning': 'nielsrolf/ow-unsloth-v2',
    'torch':  'runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04'
}

GPUs = {
    # References found at https://rest.runpod.io/v1/docs#v-0-106
    "6000Ada": "NVIDIA RTX 6000 Ada Generation",
    "4000Ada": "NVIDIA RTX 4000 Ada Generation",
    "2000Ada": "NVIDIA RTX 2000 Ada Generation",
    "A6000": "NVIDIA RTX A6000",
    "A4000": "NVIDIA RTX A4000",
    "A2000": "NVIDIA RTX A2000",
    "A100": "NVIDIA A100 80GB PCIe",  # Default A100 - 80GB
    "A100_80": "NVIDIA A100 80GB PCIe",
    "A100_40": "NVIDIA A100-SXM4-40GB",
    "A100S": "NVIDIA A100-SXM4-80GB",
    "H100": "NVIDIA H100 PCIe",
    "H100N": "NVIDIA H100 NVL",
    "H100S": "NVIDIA H100 80GB HBM3",
    "H200": "NVIDIA H200",
    "RTX4090": "NVIDIA GeForce RTX 4090",
    "A5000": "NVIDIA RTX A5000",
    "A40": "NVIDIA A40",
    "A4500": "NVIDIA RTX A4500",
    "L4": "NVIDIA L4",
    "L40": "NVIDIA L40",
    "L40S": "NVIDIA L40S",
    "RTX3080": "NVIDIA GeForce RTX 3080",
    "RTX3070": "NVIDIA GeForce RTX 3070",
    "RTX3080Ti": "NVIDIA GeForce RTX 3080 Ti",
    "A30": "NVIDIA A30",
    "RTX4080": "NVIDIA GeForce RTX 4080",
    "RTX3090": "NVIDIA GeForce RTX 3090",
    "RTX3090Ti": "NVIDIA GeForce RTX 3090 Ti",
    "V100": "Tesla V100-SXM2-32GB",  # Default V100 - 32GB
    "V100_32": "Tesla V100-SXM2-32GB",
    "V100_16": "Tesla V100-SXM2-16GB",
    "V100_16_FHHL": "Tesla V100-FHHL-16GB",
    "V100_16_PCIE": "Tesla V100-PCIE-16GB",
    "RTX4070Ti": "NVIDIA GeForce RTX 4070 Ti",
    "A4000_SFF": "NVIDIA RTX 4000 SFF Ada Generation",
    "A5000_ADA": "NVIDIA RTX 5000 Ada Generation",
    # "MI300X": "AMD Instinct MI300X OAM",
}
GPU_COUNT = 1
allowed_cuda_versions = ['12.4']


def wait_for_pod(pod, runpod_client):
    while pod.get('runtime') is None:
        time.sleep(1)
        pod = runpod_client.get_pod(pod['id'])
    return pod


@lru_cache
@backoff.on_exception(backoff.constant, Exception, interval=1, max_time=600, max_tries=600)
def get_ip_and_port(pod_id, runpod_client):
    pod = runpod_client.get_pod(pod_id)
    for ip_and_port in pod['runtime']['ports']:
        if ip_and_port['privatePort'] == 22:
            ip = ip_and_port['ip']
            port = ip_and_port['publicPort']
            return ip, port
    

def create_ssh_client(pod, runpod_client=None):
    key_file = os.path.expanduser('~/.ssh/id_ed25519')
    user='root'
    ip, port = get_ip_and_port(pod['id'], runpod_client)
    print(f'Connecting to {ip}:{port}')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for _ in range(10):
        try:
            ssh.connect(ip, port=port, username=user, key_filename=key_file)
            return ssh
        except Exception as e:
            print(e)
            time.sleep(1)
            continue
    print('Failed to connect to pod. Shutting down pod')
    runpod_client.terminate_pod(pod['id']) 

def copy_to_pod(pod, src, dst, runpod_client=None):
    if not os.path.exists(src):
        # Assume src is relative to __file__
        src = os.path.join(os.path.dirname(__file__), src)
        assert os.path.exists(src), f"File {src} does not exist"
    ssh = create_ssh_client(pod, runpod_client)
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(src, dst)

def run_on_pod(pod, cmd, runpod_client=None):
    ssh = create_ssh_client(pod, runpod_client)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    
    while True:
        line = stdout.readline()
        if not line:
            break
        print(line, end='')

    while True:
        error_line = stderr.readline()
        if not error_line:
            break
        print(error_line, end='')

    stdin.close()
    stdout.close()
    stderr.close()
    ssh.close()

def run_on_pod_interactive(pod, cmd, runpod_client=None):
    ssh = create_ssh_client(pod, runpod_client)
    channel = ssh.get_transport().open_session()
    channel.get_pty()
    channel.exec_command(cmd)
    output_buffer = b''
    logs = ''

    while True:
        if channel.recv_ready():
            output_buffer += channel.recv(1024)
            try:
                output = output_buffer.decode()
                print(output, end='')
                logs += output
                output_buffer = b''
                if "password" in output.lower():  # Check for password prompt or other interactive input requests
                    password = input("Enter the required input: ")
                    channel.send(password + '\n')
            except UnicodeDecodeError:
                pass  # Ignore decode errors and continue receiving data

        if channel.recv_stderr_ready():
            error = channel.recv_stderr(1024).decode(errors='ignore')
            print(error, end='')

        if channel.exit_status_ready():
            break

    channel.close()
    ssh.close()
    return logs
    

def check_correct_cuda(pod, allowed=allowed_cuda_versions, runpod_client=None):
    cmd = 'nvidia-smi'
    logs = run_on_pod_interactive(pod, cmd, runpod_client)
    return any([f'CUDA Version: {i}' in logs for i in allowed])


@backoff.on_exception(backoff.expo, Exception, max_time=60, max_tries=5)
def _start_worker(gpu, image, count=GPU_COUNT, name=None, container_disk_in_gb=500, volume_in_gb=500, worker_id=None, dev_mode=False, pending_workers=None, env=None, runpod_client=None):
    client = runpod_client or runpod
    gpu = GPUs.get(gpu, gpu)
    # default name: <username>-worker-<timestamp>
    name = name or f"{os.environ['USER']}-worker-{int(time.time())}"
    image = IMAGES.get(image, image)

    if pending_workers is None:
        pending_workers = []

    while True:
        env = env or {}
        env.update({
            'WORKER_ID': worker_id,
            'DOCKER_IMAGE': image,
            'OW_DEV': 'true' if dev_mode else 'false'
        })
        if worker_id is None:
            worker_id = uuid.uuid4().hex[:8]
        pod = client.create_pod(
            name, image, gpu,
            container_disk_in_gb=container_disk_in_gb,
            volume_in_gb=volume_in_gb,
            volume_mount_path='/workspace',
            gpu_count=count,
            allowed_cuda_versions=allowed_cuda_versions,
            ports="8000/http,10101/http,22/tcp",
            start_ssh=True,
            env=env
        )
        pending_workers.append(pod['id'])
        # pod = wait_for_pod(pod, client)
        
        # if not check_correct_cuda(pod, runpod_client=client):
        #     client.terminate_pod(pod['id'])
        #     continue
        
        if dev_mode:
            ip, port = get_ip_and_port(pod['id'], client)
            pending_workers.remove(pod['id'])
            return f"ssh root@{ip} -p {port} -i ~/.ssh/id_ed25519"
        else:
            pending_workers.remove(pod['id'])
            return pod


def start_worker(gpu, image, count=GPU_COUNT, name=None, container_disk_in_gb=500, volume_in_gb=500, worker_id=None, dev_mode=False, env=None, runpod_client=None):
    pending_workers = []
    if dev_mode:
        env = os.environ.copy()
    if runpod_client is None:
        runpod.api_key = os.getenv('RUNPOD_API_KEY')
        runpod_client = runpod
    try:
        pod = _start_worker(gpu, image, count, name, container_disk_in_gb, volume_in_gb, worker_id, dev_mode, pending_workers, env, runpod_client)
        return pod
    except Exception as e:
        import traceback
        traceback.print_exc()
        return None
    finally:
        print("Pending workers: ", pending_workers)
        for pod_id in pending_workers:
            print(f"Shutting down pod {pod_id}")
            runpod_client.terminate_pod(pod_id)

if __name__ == '__main__':
    fire.Fire(start_worker)