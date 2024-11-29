from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class Author(BaseModel):
    id: int
    name: str
    username: str
    state: str
    avatar_url: str
    web_url: str

class PushData(BaseModel):
    commit_count: int
    action: str
    ref_type: str
    commit_from: str
    commit_to: str
    ref: str
    commit_title: str
    ref_count: Optional[int] = None

class Project(BaseModel):
    id: int
    name: str
    description: Optional[str]
    web_url: str
    path_with_namespace: str
    created_at: datetime
    default_branch: str

class GitlabEvent(BaseModel):
    id: int
    project_id: Optional[int]
    action_name: str
    target_id: Optional[int]
    target_iid: Optional[int]
    target_type: Optional[str]
    author_id: int
    target_title: Optional[str]
    created_at: datetime
    author: Author
    push_data: Optional[PushData]
    author_username: str
    project: Optional[Project] = None
    
    class Config:
        from_attributes = True

class CommitDiff(BaseModel):
    old_path: str
    new_path: str
    diff: str

class CommitComparison(BaseModel):
    commits: List[dict]
    diffs: List[CommitDiff]
    compare_timeout: bool
    compare_same_ref: bool