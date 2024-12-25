import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Generate usage graph
def generate_graph():
    conn = sqlite3.connect("pc_usage.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, start_time, duration_seconds FROM usage_data")
    data = cursor.fetchall()
    conn.close()

    if not data:
        print("No data available to plot.")
        return

    # Extract dates and durations
    dates = [datetime.strptime(row[0], '%Y-%m-%d').date() for row in data]
    durations = [row[2] / 3600 for row in data]  # Convert seconds to hours

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(dates, durations, marker='o')
    plt.title('PC Usage Over Time')
    plt.xlabel('Date')
    plt.ylabel('Usage Duration (hours)')
    plt.grid()
    plt.show()

# Generate weekly summary
def generate_weekly_summary():
    conn = sqlite3.connect("pc_usage.db")
    cursor = conn.cursor()
    one_week_ago = datetime.now() - timedelta(days=7)
    cursor.execute("SELECT date, SUM(duration_seconds) FROM usage_data WHERE date >= ? GROUP BY date", (one_week_ago.date(),))
    data = cursor.fetchall()
    conn.close()

    print("Weekly Summary:")
    for row in data:
        print(f"Date: {row[0]}, Total Duration: {row[1] / 3600:.2f} hours")

# Generate monthly summary
def generate_monthly_summary():
    conn = sqlite3.connect("pc_usage.db")
    cursor = conn.cursor()
    one_month_ago = datetime.now() - timedelta(days=30)
    cursor.execute("SELECT date, SUM(duration_seconds) FROM usage_data WHERE date >= ? GROUP BY date", (one_month_ago.date(),))
    data = cursor.fetchall()
    conn.close()

    print("Monthly Summary:")
    for row in data:
        print(f"Date: {row[0]}, Total Duration: {row[1] / 3600:.2f} hours")

