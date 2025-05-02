import pymysql

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Saiadithya04@',  
        database='student_results',
        cursorclass=pymysql.cursors.DictCursor
    )
