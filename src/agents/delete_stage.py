import sys
from utils import remove_repo, stop_container, delete_container, delete_image, restart_nginx

args_list = sys.argv

cwd = args_list[1]
repo = args_list[2]
branch = args_list[3]

stop_container(repo, branch).communicate()
delete_container(repo, branch).communicate()
delete_image(repo, branch).communicate()
remove_repo(cwd).communicate()
restart_nginx().communicate()