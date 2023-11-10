import sys
from utils import pull, stop_container, delete_container, delete_image, build_image, run_container, restart_nginx, \
    check_for_errors
import requests


args_list = sys.argv

cwd = args_list[1]
org = args_list[2]
repo = args_list[3]
branch = args_list[4]
a_port = int(args_list[5])
e_port = int(args_list[6])

cwd = cwd+'/'+repo

requests.post('http://staginator.local/api/status/create_stage', json={
    'org': org,
    'repo': repo,
    'branch': branch,
    'status': 'pull'
})

pull_task = pull(cwd)
pull_task.communicate()
# check_for_errors(pull_task.returncode)

requests.post('http://staginator.local/api/status/create_stage', json={
    'org': org,
    'repo': repo,
    'branch': branch,
    'status': 'container_stop'
})
stop_task = stop_container(repo, branch)
stop_task.communicate()
# check_for_errors()

requests.post('http://staginator.local/api/status/create_stage', json={
    'org': org,
    'repo': repo,
    'branch': branch,
    'status': 'container_delete'
})
delete_container(repo, branch).communicate()

requests.post('http://staginator.local/api/status/create_stage', json={
    'org': org,
    'repo': repo,
    'branch': branch,
    'status': 'image_delete'
})
delete_image(repo, branch).communicate()

requests.post('http://staginator.local/api/status/create_stage', json={
    'org': org,
    'repo': repo,
    'branch': branch,
    'status': 'builds'
})
build_image(cwd, branch, repo).communicate()

requests.post('http://staginator.local/api/status/create_stage', json={
    'org': org,
    'repo': repo,
    'branch': branch,
    'status': 'run'
})
run_container(branch, repo, a_port, e_port).communicate()
restart_nginx().communicate()
