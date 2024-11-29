from datetime import datetime
from collections import defaultdict
from typing import Dict, List
import os
from .api_client import GitlabApiClient
from .models import GitlabEvent
from .config import Config

def format_events_by_project(events: List[GitlabEvent], client: GitlabApiClient) -> Dict:
    # 按项目ID分组
    project_events = defaultdict(lambda: defaultdict(list))
    
    # 获取所有涉及的项目信息
    project_cache = {}
    for event in events:
        if event.project_id and event.project_id not in project_cache:
            project = client.get_project(event.project_id)
            if project:
                project_cache[event.project_id] = project

    # 按项目和分支对事件进行分组
    for event in sorted(events, key=lambda x: x.created_at):
        if event.project_id and event.push_data:
            project = project_cache.get(event.project_id)
            if project:
                branch = event.push_data.ref
                project_events[project.name][branch].append(event)
    
    return project_events

def write_to_markdown(content: str, filename: str):
    """写入Markdown文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def generate_markdown_content(after_date: datetime, before_date: datetime, project_events: Dict, client: GitlabApiClient, show_links: bool) -> str:
    """生成Markdown格式的内容"""
    content = []
    
    # 添加标题和时间范围
    content.append("# 工作进展报告")
    content.append(f"\n## 时间范围")
    content.append(f"{after_date.date()} 至 {before_date.date()}\n")
    
    # 添加项目信息
    for project_name, branches in project_events.items():
        content.append(f"## 项目：{project_name}")
        
        for branch_name, branch_events in branches.items():
            content.append(f"\n### 分支：{branch_name}")
            
            # 统计提交数量
            total_commits = sum(e.push_data.commit_count for e in branch_events)
            content.append(f"\n- 总提交数：{total_commits}")
            
            # 显示每次提交的关键信息
            content.append("\n#### 提交记录：")
            for event in branch_events:
                commit_date = event.created_at.strftime("%Y-%m-%d %H:%M")
                commit_title = event.push_data.commit_title
                content.append(f"\n##### {commit_date} - {commit_title}")
                
                # 根据选项决定是否显示链接
                if show_links:
                    project = client.get_project(event.project_id)
                    if project and event.push_data:
                        commit_url = f"{client.base_url}/{project.path_with_namespace}/-/commit/{event.push_data.commit_to}"
                        compare_url = f"{client.base_url}/{project.path_with_namespace}/-/compare/{event.push_data.commit_from}...{event.push_data.commit_to}"
                        content.append(f"\n- [查看提交详情]({commit_url})")
                        content.append(f"\n- [查看文件对比]({compare_url})")
                
                content.append("\n---")
            
            content.append("")  # 添加空行
        
        content.append("---\n")  # 添加分隔线
    
    return "\n".join(content)

def get_gitlab_config(config: Config) -> tuple:
    """获取GitLab配置，如果没有则提示用户输入"""
    gitlab_config = config.get_gitlab_config()
    
    if gitlab_config:
        while True:
            choice = input("\n是否使用已保存的GitLab配置？(y/n): ").lower().strip()
            if choice == 'y':
                return gitlab_config['base_url'], gitlab_config['private_token']
            elif choice == 'n':
                break
            print("请输入 y 或 n")
    
    # 如果没有配置或用户选择重新输入
    print("\n请输入GitLab配置信息：")
    while True:
        base_url = input("GitLab服务地址 (例如: http://192.168.172.218): ").strip()
        if base_url and (base_url.startswith('http://') or base_url.startswith('https://')):
            break
        print("请输入有效的服务地址，需要包含 http:// 或 https://")

    while True:
        private_token = input("Private Token: ").strip()
        if private_token:
            break
        print("Token不能为空")
    
    # 保存新的配置
    config.set_gitlab_config(base_url, private_token)
    return base_url, private_token

def main():
    try:
        # 初始化配置管理
        config = Config()
        
        # 获取GitLab配置
        base_url, private_token = get_gitlab_config(config)
    
        # 创建API客户端
        client = GitlabApiClient(base_url, private_token)
        
        # 设置查询参数
        user_id = 69
        after_date = datetime(2024, 11, 21)
        before_date = datetime(2024, 11, 30)
        
        # 询问用户是否需要生成链接
        while True:
            choice = input("\n是否生成提交详情和对比链接？(y/n): ").lower().strip()
            if choice in ['y', 'n']:
                show_links = (choice == 'y')
                break
            print("请输入 y 或 n")
        
        # 获取用户事件
        print("\n正在获取提交记录...")
        events = client.get_user_events(user_id, after_date, before_date)
        project_events = format_events_by_project(events, client)
        
        # 生成Markdown内容
        print("正在生成报告...")
        markdown_content = generate_markdown_content(
            after_date, 
            before_date, 
            project_events, 
            client,
            show_links
        )
        
        # 生成文件名（使用当前时间）
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gitlab_report_{current_time}.md"
        
        # 写入文件
        write_to_markdown(markdown_content, filename)
        print(f"\n✅ 报告已生成：{filename}")
        
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")

if __name__ == "__main__":
    main() 