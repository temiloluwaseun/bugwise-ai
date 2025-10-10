# database.py
import sqlite3

# ---------- DATABASE CONNECTION ---------- #
def get_db_connection():
    conn = sqlite3.connect("bugwise.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------- CREATE TABLES ---------- #
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("✅ Database initialized successfully!")
