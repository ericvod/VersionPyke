import os
import json
from versionpyke.infra import paths

class InitRepositoryService:
    def execute(self):
        if os.path.exists(paths.VPK_DIR):
            print('Repository already initialized.')
            return

        os.makedirs(paths.COMMITS_DIR)

        with open(paths.HEAD_FILE, 'w') as f:
            f.write("")

        with open(paths.INDEX_FILE, 'w') as f:
            json.dump([], f)
        
        with open(paths.LOG_FILE, 'w') as f:
            json.dump([], f)

        print('vpk repository initialized.')