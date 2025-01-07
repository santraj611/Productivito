import os
import sqlite3
from datetime import datetime, timedelta

# constant
DATABASE_NAME = 'revision_system.db'

APP_DIR = os.path.expanduser("~/.local/state/Productivito/")
DATABASE_DIR = os.path.join(APP_DIR, "database")
DATABASE_FILE = os.path.join(DATABASE_DIR, DATABASE_NAME)

def init_db():
    """Creates the database and its directory if they don't exist."""
    try:
    # Create the application directory and database directory if they don't exist
        os.makedirs(DATABASE_DIR, exist_ok=True) # exist_ok prevents error if directory already exists
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS revisions (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           topic TEXT NOT NULL UNIQUE,
                           last_review_date DATE,
                           next_review_date DATE,
                           ease_factor REAL DEFAULT 2.5,
                           interval INTEGER DEFAULT 1
                           )
                       """)
        conn.commit()
        conn.close()

        if not DATABASE_FILE:
            print(f"Database created at: {DATABASE_FILE}")

    except OSError as e:
        print(f"Error creating directories: {e}")
    except sqlite3.Error as e:
        print(f"Error creating database: {e}")

def print_all_topics():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, last_review_date, next_review_date, topic FROM revisions")
    datas = cursor.fetchall()
    conn.commit()
    conn.close()
    print("ID \t LRD \t \t NRD \t Topic")

    for data in datas:
        print(f"{data[0]} \t {data[1]} \t {data[2]} \t {data[3]}")

def add_topic(topic):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    date = datetime.now().date()
    try:
        cursor.execute("INSERT INTO revisions (topic, next_review_date) VALUES (?, ?)", (topic, date,))
        conn.commit()
        print(f"Topic '{topic}' added.")
    except sqlite3.IntegrityError:
        print(f"Topic '{topic}' already exists.")
    conn.close()

def get_due_topics():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    date = datetime.now().date()
    cursor.execute("SELECT id, topic FROM revisions WHERE next_review_date <= ?", (date,))
    due_topics = cursor.fetchall()
    conn.close()
    return due_topics

def update_review(topic_id, quality):
    today = datetime.now().date()
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT last_review_date, next_review_date, ease_factor, interval FROM revisions WHERE id = ?
                   """, (topic_id,))
    topic_data = cursor.fetchone()
    if topic_data:
        _, next_review_date, ease_factor, interval = topic_data

        if quality >= 3: # Successful review
            interval = interval * ease_factor
            if interval < 1:
                interval = 1
            next_review_date = (datetime.now().date() + timedelta(days=int(interval))).strftime('%Y-%m-%d')
        else: # Unsuccessful Review
            interval = 1
            next_review_date = today
            ease_factor = max(1.3, ease_factor - 0.2)

        last_review_date = today
        cursor.execute("UPDATE revisions SET last_review_date = ?, next_review_date = ?, ease_factor = ?, interval = ? WHERE id = ?", (last_review_date, next_review_date, ease_factor, int(interval), topic_id))

        conn.commit()
        print("Review updated.")
    else:
        print("Topic not found.")
    conn.close()

def remove_faults():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT id, topic FROM revisions
                   """)
    data = cursor.fetchall()

    def find_empty(data: list):
        """Returns the ID of topic which is empty"""
        for items in data:
            if items[1] == '':
                return items[0]
        return False

    id = find_empty(data)
    if id != False:
        cursor.execute("DELETE FROM revisions WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        print(f"empty topic was deleted of id {id}")
    else:
        conn.commit()
        conn.close()
        print("No empty topic was found!")

def print_all_review_topics(when):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("""
                       SELECT id, last_review_date, next_review_date, topic FROM revisions
                       """)
        data = cursor.fetchall()
        conn.commit()
        conn.close()

        today = datetime.now().date()
        user_data = [] # data which user will see
        
        if when == 'Next':
            for items in data:
                if datetime.strptime(items[2], '%Y-%m-%d').date() >= today:
                    user_data.append(items)
                else:
                    continue
        elif when == 'Past':
            for items in data:
                if datetime.strptime(items[2], '%Y-%m-%d').date() < today:
                    user_data.append(items)
        else:
            print("Something went wrong!")

        # printing user_data
        print("ID \t LRD \t \t NRD \t Topic")
        for j in user_data:
            print(f"{j[0]} \t {j[1]} \t {j[2]} \t {j[3]}")

    except sqlite3.Error:
        print("Faild to get review topics")
        conn.commit()
        conn.close()

def main():
    init_db() # Create if not exists
    while True:
        print("\nRevision System")
        print("1. Add Topic")
        print("2. Review Due Topics")
        print("3. See all Topics")
        print("4. See all Next Review Topics")
        print("5. See all Last Review Topics")
        print("6. Run cleanup")
        print("7. Exit")

        choice = input("Enter choice: ").strip()

        if choice == '1':
            topic = input("Enter topic: ").strip()
            if topic:
                add_topic(topic)
            else:
                print("Try Again!")

        elif choice == '2':
            due_topics = get_due_topics()
            if due_topics:
                for topic_id, topic in due_topics:
                    print(f"\nReview: {topic}")
                    quality = int(input("How well did you remember (0-5, 5 being perfect): "))
                    update_review(topic_id, quality)
            else:
                print("No topics due for review.")
        elif choice == '3':
            print_all_topics()
        elif choice == '4':
            print_all_review_topics('Next')
        elif choice == '5':
            print_all_review_topics('Past')
        elif choice == '6':
            remove_faults()
        elif choice == '7':
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
