import os
import json
import base64
from versionpyke.infra import paths

class CheckoutService:
    def execute(self, commit_id=None):
        if not os.path.exists(paths.VPK_DIR):
            print("Repository not initialized. Run 'init' first.")
            return

        if not commit_id:
            with open(paths.HEAD_FILE, 'r') as f:
                commit_id = f.read().strip()

        if not commit_id:
            print('No commits found in HEAD.')
            return

        commit_file = None

        for filename in os.listdir(paths.COMMITS_DIR):
            if filename.startswith(commit_id):
                commit_file = os.path.join(paths.COMMITS_DIR, filename)
                break

        if not commit_file or not os.path.exists(commit_file):
            print(f'Commit {commit_id} not found.')
            return

        with open(commit_file, 'r') as f:
            commit_data = json.load(f)

        if os.path.exists(paths.HEAD_FILE):
            with open(paths.HEAD_FILE, 'r') as f:
                previous_commit_id = f.read().strip()

            if previous_commit_id and previous_commit_id != commit_data['id']:
                previous_commit_file = None

                for filename in os.listdir(paths.COMMITS_DIR):
                    if filename.startswith(previous_commit_id):
                        previous_commit_file = os.path.join(paths.COMMITS_DIR, filename)
                        break

                if previous_commit_file and os.path.exists(previous_commit_file):
                    with open(previous_commit_file, 'r') as f:
                        previous_commit_data = json.load(f)

                    for old_path in previous_commit_data['files'].keys():
                        if os.path.exists(old_path) and old_path not in commit_data['files']:
                            os.remove(old_path)

        for path, content_b64 in commit_data['files'].items():
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            with open(path, 'wb') as f:
                f.write(base64.b64decode(content_b64))

        with open(paths.HEAD_FILE, 'w') as f:
            f.write(commit_data['id'])

        print(f'Checkout for commit {commit_id[:7]} successfully completed.')