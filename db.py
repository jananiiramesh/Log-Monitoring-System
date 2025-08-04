import mysql.connector
import time

def get_connection():
    """
    Returns a connection to the 'log_system' database.
    Includes retry logic for Docker startup sequence.
    """
    max_retries = 10
    retry_delay = 5
    for attempt in range(max_retries):
        try:
            return mysql.connector.connect(
                host="mysql",  # Updated to use Docker service name
                user="root",
                password="Ak47@krishna",
                database="log_system"
            )
        except mysql.connector.Error as err:
            if attempt < max_retries - 1:
                print(f"Database connection failed: {err}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise

def create_table_if_not_exists():
    """
    Creates the logs table if it does not exist.
    The logs table stores log data along with uptime and a timestamp.
    """
    conn = get_connection()
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        topic VARCHAR(255),
        log_text TEXT,
        uptime FLOAT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()

# Optional test block: Lists tables if the module is run directly.
if __name__ == "__main__":
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    for table in cursor:
        print(table)
    cursor.close()
    conn.close()
