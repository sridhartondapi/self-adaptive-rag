from pathlib import Path
import json
import hashlib

def get_file_hash(filepath:str) -> str:
    hasher = hashlib.md5()
    with open(filepath,"rb") as f:
        for chunk in iter(lambda: f.read(4096),b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def load_previous_hashes(hash_file: str) -> dict:
    """Always return a dict, never None"""
    hash_path = Path(hash_file)
    
    if not hash_path.exists():
        return {}  # First run → empty dict
    
    try:
        with open(hash_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            else:
                print(f"Warning: Hash file {hash_file} is not a dict → starting fresh")
                return {}
    except Exception as e:
        print(f"Warning: Failed to load hash file {hash_file}: {e}")
        return {}  # Safety net
    
def save_hashes(hashes:dict, hash_file: str):
    hash_path = Path(hash_file)
    hash_path.parent.mkdir(parents=True,exist_ok=True)
    with open(hash_path, 'w', encoding='utf-8') as f:
        json.dump(hashes,f, indent=2)
