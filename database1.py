import sqlite3
from datetime import datetime


DATABASE_PATH = "access_control.db"


# --------------------------------
# Create database
# --------------------------------

def create_database():

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_access(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            authorized INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS access_logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status TEXT NOT NULL,
            score REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# --------------------------------
# Add registered user
# --------------------------------

def add_user(user_id, name, authorized):

    create_database()

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO user_access
        (id, name, authorized)
        VALUES (?, ?, ?)
        """,
        (user_id, name, authorized)
    )

    connection.commit()
    connection.close()


# --------------------------------
# Get user authorization
# --------------------------------

def get_user_access(user_id):

    create_database()

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM user_access
        WHERE id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    connection.close()

    return user


# --------------------------------
# Check authorization
# --------------------------------

def check_authorization(user_id):

    user = get_user_access(user_id)

    if user is not None:

        return user[2] == 1

    return False


# --------------------------------
# Add access log
# --------------------------------

def add_access_log(name, status, score):

    create_database()

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute(
        """
        INSERT INTO access_logs
        (name, status, score, timestamp)
        VALUES (?, ?, ?, ?)
        """,
        (
            name,
            status,
            score,
            timestamp
        )
    )

    connection.commit()
    connection.close()


# --------------------------------
# Get access logs
# --------------------------------

def get_access_logs():

    create_database()

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, status, score, timestamp
        FROM access_logs
        ORDER BY id DESC
        """
    )

    logs = cursor.fetchall()

    connection.close()

    return logs


# --------------------------------
# Local test
# --------------------------------

if __name__ == "__main__":

    create_database()

    print("Database ready.")

    print("\nAccess logs:")

    logs = get_access_logs()

    for log in logs:

        print(log)