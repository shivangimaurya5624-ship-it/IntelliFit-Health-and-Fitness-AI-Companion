import mysql.connector

# password
db_password ="......"

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=db_password,
        database="fitai_db"
    )
    cursor = conn.cursor()
    
    # add password column
    cursor.execute("ALTER TABLE users ADD COLUMN password VARCHAR(255)")
    
    conn.commit()
    print("Success! Password column added to database.")
    conn.close()

except Exception as e:
    print(f"Error: {e}")