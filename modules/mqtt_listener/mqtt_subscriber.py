import paho.mqtt.client as mqtt
import pymysql
import json
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# MySQL连接配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Root2024',
    'database': 'tianqing_db',
    'charset': 'utf8mb4'
}

# MQTT连接配置
MQTT_CONFIG = {
    'broker': '127.0.0.1',          # 改成你电脑的IP（和网关转发通道里填的一样）
    'port': 1883,
    'topic': 'tianqing',           # 改成你在网关转发通道里配置的Topic名称
    'client_id': 'tianqing_listener'
}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("MQTT连接成功")
        client.subscribe(MQTT_CONFIG['topic'])
        logging.info(f"订阅Topic: {MQTT_CONFIG['topic']}")
    else:
        logging.error(f"MQTT连接失败,返回码: {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode('utf-8'))
        logging.info(f"收到数据: {payload}")
        
        # 解析JSON，写入raw_data表
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO raw_data (timestamp, sensor_id, value, unit, data_source) VALUES (%s, %s, %s, %s, %s)",
            (payload['timestamp'], payload['sensor_id'], payload['value'], payload['unit'], 'factory')
        )
        conn.commit()
        conn.close()
        logging.info("数据已写入 raw_data 表")
        
    except json.JSONDecodeError as e:
        logging.error(f"JSON解析失败: {e}")
    except Exception as e:
        logging.error(f"数据处理失败: {e}")

def main():
    client = mqtt.Client(client_id=MQTT_CONFIG['client_id'])
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_CONFIG['broker'], MQTT_CONFIG['port'], keepalive=60)
    client.loop_forever()

if __name__ == '__main__':
    main()