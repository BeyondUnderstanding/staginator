from typing import Any, List, Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    login: str
    id: int
    node_id: str
    avatar_url: str
    gravatar_id: str
    url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    received_events_url: str
    type: str
    site_admin: bool

    
class Organization(BaseModel):
    login: str
    id: int
    node_id: str
    url: str
    repos_url: str
    events_url: str
    hooks_url: str
    issues_url: str
    members_url: str
    public_members_url: str
    avatar_url: str
    description: str


class ShortUser(BaseModel):
    name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)


class Repository(BaseModel):
    id: int
    node_id: str
    name: str
    full_name: str
    private: bool
    owner: User
    html_url: str
    description: Any
    fork: bool
    url: str
    forks_url: str
    keys_url: str
    collaborators_url: str
    teams_url: str
    hooks_url: str
    issue_events_url: str
    events_url: str
    assignees_url: str
    branches_url: str
    tags_url: str
    blobs_url: str
    git_tags_url: str
    git_refs_url: str
    trees_url: str
    statuses_url: str
    languages_url: str
    stargazers_url: str
    contributors_url: str
    subscribers_url: str
    subscription_url: str
    commits_url: str
    git_commits_url: str
    comments_url: str
    issue_comment_url: str
    contents_url: str
    compare_url: str
    merges_url: str
    archive_url: str
    downloads_url: str
    issues_url: str
    pulls_url: str
    milestones_url: str
    notifications_url: str
    labels_url: str
    releases_url: str
    deployments_url: str
    created_at: int
    updated_at: str
    pushed_at: int
    git_url: str
    ssh_url: str
    clone_url: str
    svn_url: str
    homepage: Any
    size: int
    stargazers_count: int
    watchers_count: int
    language: Any
    has_issues: bool
    has_projects: bool
    has_downloads: bool
    has_wiki: bool
    has_pages: bool
    has_discussions: bool
    forks_count: int
    mirror_url: Any
    archived: bool
    disabled: bool
    open_issues_count: int
    license: Any
    allow_forking: bool
    is_template: bool
    web_commit_signoff_required: bool
    topics: List
    visibility: str
    forks: int
    open_issues: int
    watchers: int
    default_branch: str
    stargazers: int
    master_branch: str
    organization: str


class Commit(BaseModel):
    id: str
    tree_id: str
    distinct: bool
    message: str
    timestamp: str
    url: str
    author: ShortUser
    committer: ShortUser
    added: List
    removed: List
    modified: List[str]


class PushSchema(BaseModel):
    ref: str
    before: str
    after: str
    repository: Repository
    pusher: ShortUser
    organization: Organization
    sender: User
    created: bool
    deleted: bool
    forced: bool
    base_ref: Any
    compare: str
    commits: List[Commit]
    head_commit: Commit
