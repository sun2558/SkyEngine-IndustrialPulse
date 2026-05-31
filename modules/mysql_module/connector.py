import pymysql

def test_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Root2024',
        database='tianqing_db',
        charset='utf8mb4'
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM rules')
            result = cursor.fetchone()
            print('连接成功，第一条规则是：', result)
    finally:
        connection.close()
        
test_connection()