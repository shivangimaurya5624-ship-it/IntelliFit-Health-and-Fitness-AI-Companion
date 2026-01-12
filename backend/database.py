import mysql.connector
import os

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="........",
            database="fitai_db"
        )
        return conn
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return None

# Check if connection works
if __name__ == "__main__":
    test_conn = get_db_connection()
    if test_conn:
        print("✅yes connection has been established.")
        test_conn.close()