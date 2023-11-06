import subprocess
import os
from typing import List

exc_cwd = os.getcwd() + '/src/agents'
def create_stage_execute(cwd, org, repo, git_link, branch, a_port, e_port, env: List[str]):
    with open(f'{exc_cwd}/{org}_{repo}_{branch}.env', 'a') as f:
        for s in env:
            f.write(s+'\n')

    proc = subprocess.Popen(f'python3 create_stage.py {cwd} {org} {repo} {git_link} {branch} {a_port} {e_port}', shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            cwd=exc_cwd)

def rebuild_stage_execute(cwd, org, repo, branch, a_port, e_port):
    proc = subprocess.Popen(f'python3 rebuild_stage.py {cwd} {org} {repo} {branch} {a_port} {e_port}',
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True,
                            cwd=exc_cwd)

def delete_stage_execute(cwd, repo, branch, nginx_path):
    subprocess.Popen(f'python3 delete_stage.py {cwd} {repo} {branch}',
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            cwd=exc_cwd)

    subprocess.Popen(f'rm -rf {nginx_path}',
                                        shell=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE
                                        )
