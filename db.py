import sqlite3
import os

# database path for 'applications.db'
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'applications.db')





# Initialize the database and create the applications table if it doesn't exist
# Also checks if the status is either 'Pending' or 'Rejected' and will set the default status to 'Pending'
# This function should be called once when the application starts
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





# This function will insert a new application into the database
# It takes the company name, position, and an optional status (default is 'Pending')
def insert_application(company, position, status="Pending"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO applications (company, position, status)
        VALUES (?, ?, ?)
    ''', (company, position, status))
    conn.commit()
    conn.close()





# This function will grab all applications from the database
# It returns a list of tuples containing the company name, position, and status for each application
# This can be used to display all applications in the GUI or for any other purpose
def get_all_applications():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, company, position, status FROM applications')
    rows = cursor.fetchall()
    conn.close()
    return rows






def update_application_in_db(app_id, company, position, status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE applications
        SET company = ?, position = ?, status = ?
        WHERE id = ?
    ''', (company, position, status, app_id))
    conn.commit()
    conn.close()