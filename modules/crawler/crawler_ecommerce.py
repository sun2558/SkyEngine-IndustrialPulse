import csv
import pymysql
from datetime import datetime

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='Root2024',
    database='tianqing_db',
    charset='utf8mb4'
)
cursor = connection.cursor()

with open(r'C:\VS code\tianqing_1.0.0\data\ecommerce_demo.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cursor.execute(
            "INSERT INTO raw_data (timestamp, sensor_id, value, unit) VALUES (%s, %s, %s, %s)",
            (row['timestamp'], row['sensor_id'], row['value'], row['unit'])
        )
connection.commit()
cursor.close()
connection.close()