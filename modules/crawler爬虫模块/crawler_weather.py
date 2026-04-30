import csv
import pymysql
import re
from datetime import datetime

connection = pymysql.connect(
    host='localhost',
        user='root',
        password='Root2024',
        database='tianqing_db',
        charset='utf8mb4'
)
cursor = connection.cursor()

with open(r'C:\VS code\tianqing_1.0.0\data\demo_data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # 清洗温度值
        temp_raw = row['temperature']
        match = re.search(r'[-+]?\d*\.?\d+', str(temp_raw))
        if match:
            temp_value = float(match.group())
        else:
            continue   # 不是数字就跳过这条数据
        
        cursor.execute(
            "INSERT INTO raw_data (timestamp, sensor_id, value, unit) VALUES (%s, %s, %s, %s)",
            (row['timestamp'], 'temperature', temp_value, '摄氏度')
        )
connection.commit()
cursor.close()
connection.close()