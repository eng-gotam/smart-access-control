import sqlite3


DATABASE_PATH = "access_control.db"


# --------------------------------
# Create database and tables
# --------------------------------

def create_database():

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    # Existing user table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_access(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            authorized INTEGER NOT NULL
        )
    """)

    # New access log table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS access_logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status TEXT NOT NULL,
            score REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


# --------------------------------
# Add user
# --------------------------------

def add_user(user_id, name, authorized):

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO user_access (id, name, authorized) VALUES (?, ?, ?)",
        (user_id, name, authorized)
    )

    connection.commit()
    connection.close()


# --------------------------------
# Get user
# --------------------------------

def get_user_access(user_id):

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM user_access WHERE id = ?",
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

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO access_logs (name, status, score)
        VALUES (?, ?, ?)
        """,
        (name, status, score)
    )

    connection.commit()
    connection.close()


# --------------------------------
# Get access logs
# --------------------------------

def get_access_logs():

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, status, score, timestamp
        FROM access_logs
        ORDER BY id DESC
    """)

    logs = cursor.fetchall()

    connection.close()

    return logs


# --------------------------------
# Test
# --------------------------------

if __name__ == "__main__":

    create_database()

    print("Database ready.")

    print("\nExisting user:")

    print(get_user_access(1))