import sys
from utils import clone, build_image, run_container, clearup
import requests


args_list = sys.argv

cwd = args_list[1]
org = args_list[2]
repo = args_list[3]
branch = args_list[4]
a_port = int(args_list[5])
e_port = int(args_list[6])

clone_proc = clone(cwd, repo, branch)
clone_code = clone_proc.wait()

requests.post('https://staginator.msk.beyondedge.ru/api/status/create_stage', json={
    'org': org,
    'repo': repo,
    'branch': branch,
    'status': 'clone'
})

build_proc = build_image(cwd, branch, repo)
build_code = build_proc.wait()

requests.post('https://staginator.msk.beyondedge.ru/api/status/create_stage', json={
    'org': org,
    'repo': repo,
    'branch': branch,
    'status': 'builds'
})

run_proc = run_container(branch, repo, a_port, e_port)
run_proc.wait()

requests.post('https://staginator.msk.beyondedge.ru/api/status/create_stage', json={
    'org': org,
    'repo': repo,
    'branch': branch,
    'status': 'run'
})

clearup()