import os
import json
from typing import Dict, Optional

class Config:
    def __init__(self):
        # 获取用户主目录
        self.home_dir = os.path.expanduser("~")
        # 配置文件路径
        self.config_file = os.path.join(self.home_dir, '.gitlab_report_config.json')
        self.config = self.load_config()

    def load_config(self) -> Dict:
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_config(self):
        """保存配置到文件"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2)

    def get_gitlab_config(self) -> Optional[Dict]:
        """获取GitLab配置"""
        return self.config.get('gitlab')

    def set_gitlab_config(self, base_url: str, private_token: str):
        """设置GitLab配置"""
        self.config['gitlab'] = {
            'base_url': base_url,
            'private_token': private_token
        }
        self.save_config() 