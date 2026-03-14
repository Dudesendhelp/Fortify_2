import hashlib
from pathlib import Path

db_path = Path(__file__).parent / "security_log.db"
hash_file = Path(__file__).parent / "db_hash.txt"


def compute_db_hash():

    sha256 = hashlib.sha256()

    with open(db_path, "rb") as f:
        sha256.update(f.read())

    return sha256.hexdigest()
  
  
  
  
  
def store_fingerprint():

    fingerprint = compute_db_hash()

    with open(hash_file, "w") as f:
        f.write(fingerprint)
        
        
        
        
        
def verify_integrity():

    if not hash_file.exists():
        print("No fingerprint found.")
        return True

    current_hash = compute_db_hash()

    with open(hash_file, "r") as f:
        stored_hash = f.read()

    if current_hash != stored_hash:
        print("TAMPER WARNING: Database modified!")
        return False

    print("Database integrity verified.")
    return True