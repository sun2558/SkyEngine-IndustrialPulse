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
    'broker': '你的MQTT代理IP',      # 网关到手后填
    'port': 1883,                    # 默认MQTT端口
    'topic': '你的测试Topic',         # 网关到手后填
    'client_id': 'tianqing_listener'
}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("MQTT连接成功")
        client.subscribe(MQTT_CONFIG['topic'])
        logging.info(f"订阅Topic: {MQTT_CONFIG['topic']}")
    else:
        logging.error(f"MQTT连接失败，返回码: {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode('utf-8'))
        logging.info(f"收到数据: {payload}")
        
        # TODO: 网关到手后，根据实际JSON格式写解析逻辑
        # 示例：假设payload包含 timestamp, sensor_id, value, unit
        # conn = pymysql.connect(**DB_CONFIG)
        # cursor = conn.cursor()
        # cursor.execute(
        #     "INSERT INTO raw_data (timestamp, sensor_id, value, unit) VALUES (%s, %s, %s, %s)",
        #     (payload['timestamp'], payload['sensor_id'], payload['value'], payload['unit'])
        # )
        # conn.commit()
        # conn.close()
        
    except json.JSONDecodeError as e:
        logging.error(f"JSON解析失败: {e}")
    except Exception as e:
        logging.error(f"数据处理失败: {e}")

def main():
    client = mqtt.Client(client_id=MQTT_CONFIG['client_id'])
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(MQTT_CONFIG['broker'], MQTT_CONFIG['port'], keepalive=60)
        client.loop_forever()
    except Exception as e:
        logging.error(f"MQTT连接异常: {e}")

if __name__ == '__main__':
    main()