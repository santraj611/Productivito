import time
import sqlite3
from datetime import datetime
import signal

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
def auto_save(start_time):
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

# Catch termination signals
def handle_exit(signum, frame):
    print("Application is shutting down...")
    auto_save(start_time)
    print("Session logged.")
    exit(0)


if __name__ == "__main__":
    init_db()

    signal.signal(signal.SIGTERM, handle_exit)  # Handle termination
    signal.signal(signal.SIGINT, handle_exit)  # Handle keyboard interrupt
    
    print("PC Usage Tracker Running...")
    try:
        start_time = log_start_time()
        print(f"Start time logged: {start_time}")
        while True:
            time.sleep(60)  # Check every minute to save data
            auto_save(start_time)
    except KeyboardInterrupt:
        print("Shutting down tracker...")
        print("Session logged.")
        handle_exit(None, None)

