import os
import json
from versionpyke.infra import paths

class LogService:
    def execute(self):
        if not os.path.exists(paths.VPK_DIR):
            print("Repository not initialized. Run 'init' first.")
            return

        commits = []

        for commit_file in os.listdir(paths.COMMITS_DIR):
            with open(os.path.join(paths.COMMITS_DIR, commit_file), 'r') as f:
                commit_data = json.load(f)
                commits.append(commit_data)

        commits.sort(key=lambda x: x['data'], reverse=True)

        if not commits:
            print('No commits found.')
            return

        for commit in commits:
            print(f'{commit['id'][:7]} - {commit['message']} - ({commit['data']})')