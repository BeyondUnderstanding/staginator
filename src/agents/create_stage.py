import sys
from utils import clone, build_image, run_container, clearup, create_dir, paste_env, restart_nginx
import requests


args_list = sys.argv

cwd = args_list[1]
org = args_list[2]
repo = args_list[3]
git_link = args_list[4]
branch = args_list[5]
a_port = int(args_list[6])
e_port = int(args_list[7])

env_file = open(f'{org}_{repo}_{branch}.env', 'r').read()

logger = open('create_stage.log', 'ab+')

create_dir(cwd)

requests.post('http://staginator.local/api/status/create_stage', json={
    'org': org,
    'repo': repo,
    'branch': branch,
    'status': 'clone'
})

clone_proc = clone(cwd, git_link, branch)
clone_log = clone_proc.communicate()
logger.write(clone_log[0])
logger.write(clone_log[1])

cwd = cwd+'/'+repo

paste_env(env_file, cwd)

requests.post('http://staginator.local/api/status/create_stage', json={
    'org': org,
    'repo': repo,
    'branch': branch,
    'status': 'builds'
})

build_proc = build_image(cwd, branch, repo)
build_log = build_proc.communicate()
logger.write(build_log[0])
logger.write(build_log[1])

requests.post('http://staginator.local/api/status/create_stage', json={
    'org': org,
    'repo': repo,
    'branch': branch,
    'status': 'run'
})

run_proc = run_container(branch, repo, a_port, e_port)
run_log = run_proc.communicate()
logger.write(run_log[0])
logger.write(run_log[1])

clearup()

logger.close()
restart_nginx().communicate()
