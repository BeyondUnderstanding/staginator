import sys
from utils import (clone, build_image, run_container,
                   clearup, create_dir, paste_env,
                   restart_nginx, write_logger, post_log,
                   change_status)


args_list = sys.argv

cwd = args_list[1]
org = args_list[2]
repo = args_list[3]
git_link = args_list[4]
branch = args_list[5]
a_port = int(args_list[6])
e_port = int(args_list[7])

env_file = open(f'{org}_{repo}_{branch}.env', 'r').read()

logger = open(f'create_{org}_{repo}_{branch}.log', 'ab+')


change_status(org, repo, branch,
              status='mkdir_t')
cd_t = create_dir(cwd)
write_logger(logger, cd_t.communicate())
if cd_t.returncode != 0:
    post_log(org, repo, branch,
             message='Error: Create directory task returned non zero return code')
    exit(1)


change_status(org, repo, branch,
              status='clone_t')
clone_proc = clone(cwd, git_link, branch)
write_logger(logger, clone_proc.communicate())
if clone_proc.returncode != 0:
    post_log(org, repo, branch,
             message='Error: Clone repository task returned non zero return code')
    exit(1)


cwd = cwd+'/'+repo


paste_env(env_file, cwd)


change_status(org, repo, branch,
              status='build_t')
build_proc = build_image(cwd, branch, repo)
write_logger(logger, build_proc.communicate())
if build_proc.returncode != 0:
    post_log(org, repo, branch,
             message='Error: Build container task returned non zero return code')
    exit(1)


change_status(org, repo, branch,
              status='run_t')
run_proc = run_container(branch, repo, a_port, e_port)
write_logger(logger, run_proc.communicate())
if run_proc.returncode != 0:
    post_log(org, repo, branch,
             message='Error: Run container task returned non zero return code')
    exit(1)


clearup()


change_status(org, repo, branch,
              status='nginx_t')
ng_t = restart_nginx()
write_logger(logger, ng_t.communicate())
if ng_t.returncode != 0:
    post_log(org, repo, branch,
             message='Error: Restart nginx task returned non zero return code')
    exit(1)


change_status(org, repo, branch,
              status='run')

