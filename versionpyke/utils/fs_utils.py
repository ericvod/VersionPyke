import os
from versionpyke.infra.paths import VPK_DIR

def get_all_files():
    files = []

    for root, _, filenames in os.walk('.'):
        if VPK_DIR in root:
            continue

        for file in filenames:
            path = os.path.join(root, file)

            if path.startswith(f'./{VPK_DIR}'):
                continue

            files.append(path)
    
    return files