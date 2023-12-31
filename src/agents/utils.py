import subprocess
from typing import BinaryIO

import requests

def post_log(org: str, repo: str, branch: str, message: str):
    requests.post('http://staginator.local/api/status', json={
        'org': org,
        'repo': repo,
        'branch': branch,
        'message': message
    })

def change_status(org: str, repo: str, branch: str, status: str):
    requests.patch('http://staginator.local/api/status', json={
        'org': org,
        'repo': repo,
        'branch': branch,
        'status': status
    })

def write_logger(logger: BinaryIO, thread: tuple[bytes, bytes]):
    logger.write(thread[0])
    logger.write(thread[1])


def create_dir(cwd: str):
    proc = subprocess.Popen(f'mkdir {cwd}', shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                            )
    return proc

def clone(cwd: str, repo: str, branch: str):
    proc = subprocess.Popen(f'git clone --branch {branch} {repo}', shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            cwd=cwd)
    return proc


def pull(cwd: str):
    proc = subprocess.Popen('git pull', shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            cwd=cwd)
    return proc


def remove_repo(cwd):
    proc = subprocess.Popen(f'rm -r {cwd}', shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                            )
    return proc


def build_image(cwd: str, branch: str, repo: str):
    proc = subprocess.Popen(f'docker build -t staginator-{repo}-{branch} .', shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            cwd=cwd)
    return proc


def run_container(branch: str, repo: str, a_port: int, e_port: int):
    proc = subprocess.Popen(f'docker run -d --name staginator-{repo}-{branch} -p 10.1.0.1:{a_port}:{e_port} staginator-{repo}-{branch}', shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                            )
    return proc

def stop_container(repo: str, branch: str):
    proc = subprocess.Popen(
        f'docker stop staginator-{repo}-{branch}', shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return proc

def delete_container(repo: str, branch: str):
    proc = subprocess.Popen(
        f'docker rm staginator-{repo}-{branch}', shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return proc

def get_logs(repo: str, branch: str):
    proc = subprocess.Popen(
        f'docker logs staginator-{repo}-{branch}', shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return proc

def clearup():
    proc = subprocess.run(
        f'docker system prune -f', shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
        )
    return proc

def paste_env(env: str, cwd: str):
    env_file = open(f'{cwd}/.env', 'w')
    env_file.write(env)
    env_file.close()


def delete_image(repo: str, branch: str):
    proc = subprocess.Popen(
        f'docker image rm staginator-{repo}-{branch}', shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return proc

def restart_nginx():
    proc = subprocess.Popen(
        f'service nginx restart', shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return proc

def check_for_errors():
    exit()