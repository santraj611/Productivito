import os
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from io import BytesIO
from threading import Thread

# constant
DATABASE_NAME = 'pc_usage.db'

APP_DIR = os.path.expanduser("~/.local/state/Productivito/")
DATABASE_DIR = os.path.join(APP_DIR, "database")
DATABASE_FILE = os.path.join(DATABASE_DIR, DATABASE_NAME)

# Generate usage graph
def generate_graph():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT date, start_time, SUM(duration_seconds) FROM usage_data")
    data = cursor.fetchall()
    conn.close()

    if not data:
        print("No data available to plot.")
        return

    # Extract dates and durations
    dates = [datetime.strptime(row[0], '%Y-%m-%d').date() for row in data]
    ddates = []
    for date in dates:
        _, m, d = str(date).split('-')
        ndate = m + '-' + d
        ddates.append(ndate)

    durations = [row[2] / 3600 for row in data]  # Convert seconds to hours

    # Plot
    plt.figure(figsize=(15, 5))
    plt.bar(dates, durations, width=1.0, edgecolor='white', linewidth=0.7, color="#80FFEC")
    plt.title('PC Usage Over Time')
    plt.xlabel('Date')
    plt.ylabel('Usage Duration (hours)')
    plt.grid()

    # plt.show()

    graph_image = BytesIO()  # Create a buffer to store the image data

    # Save the graph as an image
    graph_path = "static/usage_graph.png"
    plt.savefig(graph_path)
    plt.close()
    graph_image.seek(0)  # Rewind the buffer to the beginning
    return graph_path


# Generate weekly summary
def generate_weekly_summary():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    one_week_ago = datetime.now() - timedelta(days=7)
    cursor.execute("SELECT date, SUM(duration_seconds) FROM usage_data WHERE date >= ? GROUP BY date", (one_week_ago.date(),))
    data = cursor.fetchall()
    conn.close()

    if not data:
        print("No data available to plot.")
        return

    # Extract dates and durations
    dates = [datetime.strptime(row[0], '%Y-%m-%d').date() for row in data]
    durations = [row[1] / 3600 for row in data]  # Convert seconds to hours

    # Plot
    plt.figure(figsize=(10, 5))
    plt.bar(dates, durations, color="#80FFEC")

    # plt.plot(dates, durations, marker='o')
    plt.title('PC Usage Over Week')
    plt.xlabel('Date')
    plt.ylabel('Usage Duration (hours)')
    plt.grid()

    # plt.show()

    # Save the graph as an image
    graph_path = "static/weekly_usage_graph.png"
    plt.savefig(graph_path)
    plt.close()
    return graph_path

    # print("Weekly Summary:")
    # for row in data:
    #     print(f"Date: {row[0]}, Total Duration: {row[1] / 3600:.2f} hours")

# Generate monthly summary
def generate_monthly_summary():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    one_month_ago = datetime.now() - timedelta(days=30)
    cursor.execute("SELECT date, SUM(duration_seconds) FROM usage_data WHERE date >= ? GROUP BY date", (one_month_ago.date(),))
    data = cursor.fetchall()
    conn.close()

    if not data:
        print("No data available to plot.")
        return

    # Extract dates and durations
    dates = [datetime.strptime(row[0], '%Y-%m-%d').date() for row in data]
    durations = [row[1] / 3600 for row in data]  # Convert seconds to hours

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(dates, durations, marker='o')
    plt.title('PC Usage Over Month')
    plt.xlabel('Date')
    plt.ylabel('Usage Duration (hours)')
    plt.grid()
    # plt.show()

    # Save the graph as an image
    graph_path = "static/monthly_usage_graph.png"
    plt.savefig(graph_path)
    plt.close()
    return graph_path

    # print("Monthly Summary:")
    # for row in data:
    #     print(f"Date: {row[0]}, Total Duration: {row[1] / 3600:.2f} hours")

