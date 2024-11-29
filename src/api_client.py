import requests
from datetime import datetime
from typing import List, Optional, Dict
from .models import GitlabEvent, Project, CommitComparison

class GitlabApiClient:
    def __init__(self, base_url: str, private_token: str):
        self.base_url = base_url
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'PRIVATE-TOKEN': private_token,
            'User-Agent': 'PostmanRuntime-ApipostRuntime/1.1.0'
        }

    def get_user_events(self, user_id: int, after: datetime, before: datetime) -> List[GitlabEvent]:
        url = f"{self.base_url}/api/v4/users/{user_id}/events"
        
        params = {
            'after': after.strftime('%Y-%m-%d'),
            'before': before.strftime('%Y-%m-%d'),
            'sort': 'asc'
        }

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        events = [GitlabEvent.model_validate(event) for event in response.json()]
        return events

    def get_project(self, project_id: int) -> Optional[Project]:
        """获取项目详情"""
        url = f"{self.base_url}/api/v4/projects/{project_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return Project.model_validate(response.json())
        except Exception as e:
            print(f"获取项目 {project_id} 详情失败: {str(e)}")
            return None

    def get_commit_comparison(self, project_id: int, from_commit: str, to_commit: str) -> Optional[CommitComparison]:
        """获取两个提交之间的差异"""
        url = f"{self.base_url}/api/v4/projects/{project_id}/repository/compare"
        params = {
            'from': from_commit,
            'to': to_commit
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return CommitComparison.model_validate(response.json())
        except Exception as e:
            print(f"获取提交对比失败: {str(e)}")
            return None