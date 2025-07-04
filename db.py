import sqlite3
import os

# database path for 'applications.db'
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'applications.db')






def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            position TEXT NOT NULL,
            status TEXT CHECK(status IN ('Pending', 'Rejected')) NOT NULL DEFAULT 'Pending'
        )
    ''')
    conn.commit()
    conn.close()






def insert_application(company, position, status="Pending"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO applications (company, position, status)
        VALUES (?, ?, ?)
    ''', (company, position, status))
    conn.commit()
    conn.close()






def get_all_applications():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT company, position, status FROM applications')
    rows = cursor.fetchall()
    conn.close()
    return rows