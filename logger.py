from database1 import create_database, add_access_log, get_access_logs


# --------------------------------
# Log access event
# --------------------------------

def log_access(name, status, score):

    add_access_log(
        name,
        status,
        score
    )

    print(
        f"LOGGED: {name} | {status} | Score: {score:.2f}"
    )


# --------------------------------
# Show access history
# --------------------------------

def show_logs():

    logs = get_access_logs()

    if not logs:
        print("No access logs found.")
        return

    print("\nAccess History")
    print("-" * 60)

    for log in logs:

        log_id, name, status, score, timestamp = log

        print(
            f"{log_id} | "
            f"{name} | "
            f"{status} | "
            f"{score:.2f} | "
            f"{timestamp}"
        )


# --------------------------------
# Test logger
# --------------------------------

if __name__ == "__main__":

    create_database()

    print("Testing logger...")

    log_access(
        "Gotam",
        "AUTHORIZED",
        0.67
    )

    log_access(
        "Unknown",
        "UNAUTHORIZED",
        0.34
    )

    show_logs()