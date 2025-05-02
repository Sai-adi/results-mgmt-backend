from db import get_connection

try:
    connection = get_connection()
    print("Database connection successful!")
except Exception as e:
    print("Database connection failed!")
    print(e)
finally:
    if connection:
        connection.close()
        print("Database connection closed.")