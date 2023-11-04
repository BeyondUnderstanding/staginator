from typing import List

from fastapi import APIRouter
from src.modules.githubmanager import github
from src.modules.stage.schema import RemoteRepoSchema, RemoteBranchSchema, RemoteOrgSchema

github_repos = APIRouter(prefix='/github')


@github_repos.get('/list_orgs', description='List available GitHub orgs', response_model=List[RemoteOrgSchema])
async def list_orgs():
    return github.get_user().get_orgs()


@github_repos.get('/list_repos', description='List available GitHub repos in org', response_model=List[RemoteRepoSchema])
async def list_repo(org: str):
    return github.get_organization(org).get_repos()


@github_repos.get('/list_branches', description='List available branches by repo', response_model=List[RemoteBranchSchema])
async def list_branches(repo: str, org: str):
    return github.get_organization(org).get_repo(repo).get_branches()
