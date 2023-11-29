import sys
from utils import pull, stop_container, delete_container, delete_image, build_image, run_container, restart_nginx, \
    post_log, write_logger, change_status


args_list = sys.argv

cwd = args_list[1]
org = args_list[2]
repo = args_list[3]
branch = args_list[4]
a_port = int(args_list[5])
e_port = int(args_list[6])

cwd = cwd+'/'+repo
logger = open(f'rebuild_{org}_{repo}_{branch}.log', 'ab+')


change_status(org, repo, branch,
              status='pull_t')
pull_task = pull(cwd)
write_logger(logger, pull_task.communicate())
if pull_task.returncode != 0:
    post_log(org, repo, branch,
             message='Error: Pull Task returned non zero return code')
    exit(1)


change_status(org, repo, branch,
              status='stop_t')
stop_task = stop_container(repo, branch)
write_logger(logger, stop_task.communicate())
if stop_task.returncode != 0:
    post_log(org, repo, branch,
             message='Error: Stop container task returned non zero return code')
    exit(1)


change_status(org, repo, branch,
              status='delete_1_t')
delete_container_task = delete_container(repo, branch)
write_logger(logger, delete_container_task.communicate())
if delete_container_task.returncode != 0:
    post_log(org, repo, branch,
             message='Error: Delete container task returned non zero return code')


change_status(org, repo, branch,
              status='delete_2_t')
delete_image_task = delete_image(repo, branch)
write_logger(logger, delete_image_task.communicate())
if delete_image_task.returncode != 0:
    post_log(org, repo, branch,
             message='Error: Delete image task returned non zero return code')


change_status(org, repo, branch,
              status='build_t')
build_image_task = build_image(cwd, branch, repo)
write_logger(logger, build_image_task.communicate())
if build_image_task.returncode != 0:
    post_log(org, repo, branch,
             message='Error: Build image task returned non zero return code')
    exit(1)


change_status(org, repo, branch,
              status='run_t')
run_container_task = run_container(branch, repo, a_port, e_port)
write_logger(logger, run_container_task.communicate())
if run_container_task.returncode != 0:
    post_log(org, repo, branch,
             message='Error: Run container task returned non zero return code')
    exit(1)
change_status(org, repo, branch,
              status='run')
