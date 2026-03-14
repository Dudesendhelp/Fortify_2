import sqlite3

def init_db():
    conn = sqlite3.connect("security_log.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS security_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        event_type TEXT NOT NULL,
        security_score INTEGER
    )
    """)

    conn.commit()
    conn.close()
    
if __name__=="__main__":
    init_db()