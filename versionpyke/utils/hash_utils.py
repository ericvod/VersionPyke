import hashlib
import time

def generate_id_commit(content_bytes):
    return hashlib.sha1(content_bytes + str(time.time()).encode()).hexdigest()