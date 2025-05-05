import os
import json
from versionpyke.infra import paths

class AddService:
    def execute(self, files):
        if not os.path.exists(paths.VPK_DIR):
            print("Repository not initialized. Run 'init' first.")
            return
        
        if not files:
            print("No files specified to add.")
            return
        
        if os.path.exists(paths.INDEX_FILE):
            with open(paths.INDEX_FILE, 'r') as f:
                index = json.load(f)
        else:
            index = []
        
        added_files = []

        for file_path in files:
            normalized_path = os.path.normpath(os.path.relpath(file_path))
            if not os.path.exists(normalized_path):
                print(f'[warning] File not found: {file_path}')
                continue

            if normalized_path not in index:
                index.append(normalized_path)
                added_files.append(normalized_path)
        
        with open(paths.INDEX_FILE, 'w') as f:
            json.dump(index, f, indent=2)

        if added_files:
            print('Files added to stagind area:')
            for f in added_files:
                print(f'  {f}')
        else:
            print('No new files added.')