import os
import json
import base64
from versionpyke.infra import paths
from versionpyke.utils import fs_utils

class StatusService:
    def execute(self):
        if not os.path.exists(paths.VPK_DIR):
            print("Repository not initialized. Run 'init' first.")
            return

        current_snapshot = self._get_current_snapshot()
        staged_files = self._load_staged_files()

        if not self._head_exists():
            self._print_status_without_commit(current_snapshot, staged_files)
            return

        last_snapshot = self._load_last_commit_snapshot()

        if last_snapshot is None:
            print("Invalid HEAD commit. Cannot determine status.")
            return

        self._print_status(current_snapshot, last_snapshot, staged_files)

    def _get_current_snapshot(self):
        snapshot = {}

        for path in fs_utils.get_all_files():
            normalized_path = os.path.normpath(os.path.relpath(path))

            with open(path, 'rb') as f:
                snapshot[normalized_path] = base64.b64encode(f.read()).decode()

        return snapshot

    def _load_staged_files(self):
        if os.path.exists(paths.INDEX_FILE):
            with open(paths.INDEX_FILE, 'r') as f:
                return json.load(f)
            
        return []

    def _head_exists(self):
        return os.path.exists(paths.HEAD_FILE) and os.path.getsize(paths.HEAD_FILE) > 0

    def _load_last_commit_snapshot(self):
        with open(paths.HEAD_FILE, 'r') as f:
            commit_id = f.read().strip()

        for filename in os.listdir(paths.COMMITS_DIR):
            if filename.startswith(commit_id):
                with open(os.path.join(paths.COMMITS_DIR, filename), 'r') as f:
                    data = json.load(f)
                    return data['files']
                
        return None

    def _print_status_without_commit(self, current_snapshot, staged_files):
        if staged_files:
            print("Changes staged for commit:")

            for path in staged_files:
                print(f"  staged:     {path}")

        untracked = [path for path in current_snapshot if path not in staged_files]

        if untracked:
            print('Untracked files:')
            for path in untracked:
                print(f'  untracked:  {path}')
        elif not staged_files:
            print('Working directory clean.')

    def _print_status(self, current_snapshot, last_snapshot, staged_files):
        staged = []
        modified = []
        deleted = []
        untracked = []

        for path, old_content in last_snapshot.items():
            if path not in current_snapshot:
                deleted.append(path)
            elif old_content != current_snapshot[path]:
                if path in staged_files:
                    staged.append(path)
                else:
                    modified.append(path)

        for path in current_snapshot:
            if path not in last_snapshot and path not in staged_files:
                untracked.append(path)

        if staged:
            print('Changes staged for commit:')
            for path in staged:
                print(f'  staged:     {path}')

        if modified:
            print('Changes not staged for commit:')
            for path in modified:
                print(f'  modified:   {path}')

        if deleted:
            print('Deleted files:')
            for path in deleted:
                print(f'  deleted:    {path}')

        if untracked:
            print('Untracked files:')
            for path in untracked:
                print(f'  untracked:  {path}')

        if not staged and not modified and not deleted and not untracked:
            print('Working directory clean.')
