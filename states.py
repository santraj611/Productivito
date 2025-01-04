import sqlite3
from datetime import datetime, timedelta

def get_date():
    """Return: date of today"""
    # datetime.strptime(row[0], '%Y-%m-%d').date() for row in data
    today = datetime.strptime(str(datetime.now().date()), '%Y-%m-%d').date()
    return today

def get_week():
    """Return: date of one week ago"""
    one_week_ago = datetime.now() - timedelta(days=7)
    one_week_ago, _ = str(one_week_ago).split(' ')
    # print(one_week_ago)
    return one_week_ago

def get_month():
    """Return: date of one month ago"""
    one_month_ago = datetime.now() - timedelta(days=30)
    one_month_ago, _ = str(one_month_ago).split(' ')
    # print(one_month_ago)
    return one_month_ago

def total_screen_time(day: str):
    """Returns total usage on/from the given day
    Parameters:
    day: String

    Return:
    Total usage: Float
    """
    try:
        conn = sqlite3.connect("pc_usage.db")
        cursor = conn.cursor()
        query = f"SELECT SUM(duration_seconds) FROM usage_data WHERE date >= ?"

        cursor.execute(query, (day,))
        result = cursor.fetchone()
        conn.close()

        if result:
            hours = result[0] / 3600 # convert seconds to hours
            # print(f" Hours in the day {hours}")
            return hours
        else:
            print("No data")
            return 0

    except Exception:
        print("Failed to get today's total usage")
        return 0

# if __name__ == '__main__':

    # today = str(get_date())
    # usage = total_screen_time(today)
    # print(f"Screen time( Hours ):\t {usage:.2f}")
