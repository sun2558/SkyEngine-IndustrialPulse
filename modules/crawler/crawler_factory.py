import csv
import pymysql
from datetime import datetime, timedelta
import random

# 生成模拟工业数据（温度、压力、振动）
def generate_factory_csv():
    with open('data/factory_demo.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'sensor_id', 'value', 'unit'])
        start_time = datetime(2026, 5, 1, 8, 0, 0)
        for i in range(500):
            timestamp = start_time + timedelta(minutes=i)
            # 温度：正常20-35度，偶尔异常
            temp = random.uniform(20, 35) if random.random() > 0.05 else random.uniform(80, 100)
            writer.writerow([timestamp, 'temperature', round(temp, 2), '摄氏度'])
            # 压力：正常0.8-1.2MPa，偶尔异常
            pressure = random.uniform(0.8, 1.2) if random.random() > 0.05 else random.uniform(2.0, 3.0)
            writer.writerow([timestamp, 'pressure', round(pressure, 2), 'MPa'])
            # 振动：正常0-5mm/s，偶尔异常
            vibration = random.uniform(0, 5) if random.random() > 0.05 else random.uniform(15, 25)
            writer.writerow([timestamp, 'vibration', round(vibration, 2), 'mm/s'])

# 生成文件
generate_factory_csv()
print("工厂模拟数据已生成: data/factory_demo.csv")

# 连接数据库并插入数据
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='Root2024',
    database='tianqing_db',
    charset='utf8mb4'
)
cursor = conn.cursor()

with open('data/factory_demo.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cursor.execute(
            "INSERT INTO raw_data (timestamp, sensor_id, value, unit) VALUES (%s, %s, %s, %s)",
            (row['timestamp'], row['sensor_id'], row['value'], row['unit'])
        )
conn.commit()
cursor.close()
conn.close()
print("工厂数据已写入 raw_data 表")