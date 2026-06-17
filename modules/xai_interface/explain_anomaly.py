import pymysql
import json

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='Root2024',
    database='tianqing_db',
    charset='utf8mb4'
)
cursor = conn.cursor()

# 联表查询：异常记录 + 对应的规则类型和参数
cursor.execute("""
    SELECT c.id, c.value, r.rule_type, r.params
    FROM cleaned_data c
    JOIN rules r ON c.rule_id = r.id
    WHERE c.is_anomaly = True
""")
anomalies = cursor.fetchall()

def generate_explanation(value):
    """根据数值生成业务层面的解释和建议"""
    if value >= 900:
        return {
            'reason': f'温度{value}℃：传感器可能断线或短路，请检查传感器连接和线路',
            'suggestion': '检查传感器接线、更换传感器或校准设备'
        }
    elif value <= -40:
        return {
            'reason': f'温度{value}℃：传感器可能冻结或损坏，请检查传感器状态和环境温度',
            'suggestion': '检查传感器是否被冻住、更换传感器或调整安装位置'
        }
    elif -10 <= value < 0:
        return {
            'reason': f'温度{value}℃：温度异常偏低，可能存在设备未启动或冷媒泄漏',
            'suggestion': '检查设备运行状态、排查冷媒系统'
        }
    elif value >= 80:
        return {
            'reason': f'温度{value}℃：温度持续偏高，可能存在散热不良或工艺参数异常',
            'suggestion': '检查散热系统、清理积灰、核对工艺设定值'
        }
    elif value >= 70:
        return {
            'reason': f'温度{value}℃：温度偏高，建议关注设备运行状态',
            'suggestion': '观察设备运行、检查冷却系统'
        }
    else:
        return {
            'reason': f'温度{value}℃：偏离正常范围，建议检查设备或工艺参数',
            'suggestion': '检查设备状态、核对工艺参数'
        }

for anomaly in anomalies:
    data_id, value, rule_type, params_str = anomaly
    params = json.loads(params_str) if params_str else {}
    result = generate_explanation(value)
    reason = result['reason']
    suggestion = result['suggestion']
    print(f"ID {data_id}: {reason} -> 建议: {suggestion}")
    cursor.execute(
        "INSERT INTO explanations (cleaned_data_id, anomaly_reason, suggestion) VALUES (%s, %s, %s)",
        (data_id, reason, suggestion)
    )

conn.commit()
cursor.close()
conn.close()
print("完成：已生成业务解释和建议")