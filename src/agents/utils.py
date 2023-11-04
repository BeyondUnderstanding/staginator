import subprocess


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
    proc = subprocess.Popen(f'docker run -d --name staginator-{repo}-{branch} -p {a_port}:{e_port} staginator-{repo}-{branch}', shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                            )
    return proc

def stop_container(branch: str, repo: str):
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


def clearup():
    proc = subprocess.Popen(
        f'docker system prune', shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
        )
    return proc
