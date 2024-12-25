import os
import time
import sqlite3
from datetime import datetime

# Database setup
def init_db():
    conn = sqlite3.connect("pc_usage.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usage_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            start_time DATETIME,
            end_time DATETIME,
            duration_seconds INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Record start time
def log_start_time():
    start_time = datetime.now()
    return start_time

# Record end time and save to DB
def log_end_time(start_time):
    end_time = datetime.now()
    duration_seconds = int((end_time - start_time).total_seconds())
    date = start_time.date()
    conn = sqlite3.connect("pc_usage.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO usage_data (date, start_time, end_time, duration_seconds) VALUES (?, ?, ?, ?)",
        (date, start_time, end_time, duration_seconds)
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    
    print("PC Usage Tracker Running...")
    try:
        start_time = log_start_time()
        print(f"Start time logged: {start_time}")
        while True:
            time.sleep(1)  # Simulate the app running
    except KeyboardInterrupt:
        print("Shutting down tracker...")
        log_end_time(start_time)
        print("Session logged.")
        # generate_graph()

