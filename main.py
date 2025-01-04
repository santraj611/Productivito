import time
import sqlite3
from datetime import datetime
import signal
import psutil

# Database setup
def init_db():
    """Createrd or looks for Database"""
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
    """Logs the start Time"""
    start_time = datetime.now()
    return start_time

# Record end time and save to DB
def auto_save(start_time):
    """Auto saves Time"""
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

# Checks if the user is Active or not?
def is_user_active() -> bool:
    """
    Checks if the user is actively interacting with the computer.

    Returns:
        bool: True if the user is active, False otherwise.
    """
    # Get initial CPU usage and disk I/O counters
    initial_cpu_usage = psutil.cpu_percent(interval=1)
    initial_disk_read = psutil.disk_io_counters().read_bytes
    initial_disk_write = psutil.disk_io_counters().write_bytes

    time.sleep(5)  # Wait for a short interval

    # Get current CPU usage and disk I/O counters
    current_cpu_usage = psutil.cpu_percent(interval=1)
    current_disk_read, current_disk_write = psutil.disk_io_counters().read_bytes, psutil.disk_io_counters().write_bytes

    # Calculate changes in CPU usage and disk I/O
    cpu_usage_delta = abs(current_cpu_usage - initial_cpu_usage)
    disk_read_delta = current_disk_read - initial_disk_read
    disk_write_delta = current_disk_write - initial_disk_write

    # Define thresholds for inactivity
    cpu_idle_threshold = 5  # Example: CPU usage below 5%
    disk_idle_threshold = 1024  # Example: Less than 1KB of disk activity

    return cpu_usage_delta > cpu_idle_threshold or disk_read_delta > disk_idle_threshold or disk_write_delta > disk_idle_threshold



if __name__ == "__main__":
    init_db()

    signal.signal(signal.SIGTERM, handle_exit)  # Handle termination
    signal.signal(signal.SIGINT, handle_exit)  # Handle keyboard interrupt
    
    print("PC Usage Tracker Running...")

    try:
        while True:
            start_time = log_start_time() # starting timer every 10 minute
            # time.sleep(600)  # Check every 10 minute to save data
            auto_save(start_time)

            # Intented code is not working as expected 
            if is_user_active():
                time.sleep(60)  # Check every minute to save data
                auto_save(start_time)
            else:
                # User went offline...
                time.sleep(60)
                continue

    except KeyboardInterrupt:
        print("Shutting down tracker...")
        print("Session logged.")
        handle_exit(None, None)

