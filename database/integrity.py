import hashlib
import sys
from pathlib import Path


# Detect correct storage directory
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent / "App_data"
else:
    BASE_DIR = Path(__file__).resolve().parent / "database"

# Create folder if it doesn't exist
BASE_DIR.mkdir(parents=True, exist_ok=True)

# File paths
db_path = BASE_DIR / "security_log.db"
hash_file = BASE_DIR / "db_hash.txt"


def compute_db_hash():
    sha256 = hashlib.sha256()

    # Create database if it doesn't exist
    if not db_path.exists():
        db_path.touch()

    # Hash database file
    with open(db_path, "rb") as f:
        while chunk := f.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()


def store_fingerprint():
    fingerprint = compute_db_hash()

    with open(hash_file, "w") as f:
        f.write(fingerprint)


def verify_integrity():

    # First run (no fingerprint yet)
    if not hash_file.exists():
        store_fingerprint()
        print("No fingerprint found. Creating one.")
        return True

    current_hash = compute_db_hash()

    with open(hash_file, "r") as f:
        stored_hash = f.read().strip()

    if current_hash != stored_hash:
        print("⚠️ TAMPER WARNING: Database modified!")
        return False

    print("Database integrity verified.")
    return True