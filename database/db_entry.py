from datetime import datetime
import sqlite3
from pathlib import Path
import sys


def _get_db_path() -> Path:
    """
    Return the path to the SQLite DB both in dev and when frozen as an EXE.
    In dev:    <project_root>/database/security_log.db
    In EXE:    <folder_with_exe>/database/security_log.db
    """
    if getattr(sys, "frozen", False):
        # Running from a bundled EXE
        base_dir = Path(sys.executable).parent / "App_data"
    else:
        # Running from source
        base_dir = Path(__file__).parent

    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir / "security_log.db"


def log_event(event_type: str, security_score: int) -> None:
    db_path = _get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ensure table exists
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS security_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            event_type TEXT NOT NULL,
            security_score INTEGER NOT NULL
        )
        """
    )

    timestamp = datetime.now().isoformat()

    cursor.execute(
        "INSERT INTO security_events (timestamp, event_type, security_score) VALUES (?, ?, ?)",
        (timestamp, event_type, security_score),
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    log_event("password_check", 16)