import os
import json
import time
import base64
from versionpyke.infra import paths
from versionpyke.utils import hash_utils, fs_utils

class CommitService:
    def execute(self, message):
        if not os.path.exists(paths.VPK_DIR):
            print("Repository not initialized. Run 'init' first.")
            return
        
        if not os.path.exists(paths.INDEX_FILE):
            print("No files staged. Use 'vpk add <file>' to stage files.")
            return

        with open(paths.INDEX_FILE, 'r') as f:
            staged_files = json.load(f)

        if not staged_files:
            print('Staging area is empty. Nothing to commit.')
            return
        
        snapshot = {}

        for path in staged_files:
            if not os.path.exists(path):
                continue

            with open(path, 'rb') as f:
                content = f.read()
                snapshot[path] = base64.b64encode(content).decode()

        snapshot_bytes = json.dumps(snapshot, sort_keys=True).encode()
        id_commit = hash_utils.generate_id_commit(snapshot_bytes)

        commit_obj = {
            "id": id_commit,
            "message": message,
            "data": time.strftime('%d-%m-%Y %H:%M:%S'),
            "files": snapshot,
        }

        commit_path = os.path.join(paths.COMMITS_DIR, f'{id_commit}.json')

        with open(commit_path, 'w') as f:
            json.dump(commit_obj, f, indent=2)

        with open(paths.HEAD_FILE, 'w') as f:
            f.write(id_commit)

        with open(paths.LOG_FILE, 'r+') as f:
            log = json.load(f)
            log.append({"id": id_commit, "message": message, "data": commit_obj["data"]})
            f.seek(0)
            json.dump(log, f, indent=2)

        with open(paths.INDEX_FILE, 'w') as f:
            json.dump([], f)

        print(f'Commit created: {id_commit[:7]} - {message}') 