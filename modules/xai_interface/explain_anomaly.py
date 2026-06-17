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

def generate_explanation(value, rule_type):
    """根据数值和规则类型生成业务解释，并保留触发规则信息"""
    # 先根据数值确定业务描述
    if value >= 900:
        reason = f'温度{value}℃：传感器可能断线或短路，请检查传感器连接和线路'
        suggestion = '检查传感器接线、更换传感器或校准设备'
    elif value <= -40:
        reason = f'温度{value}℃：传感器可能冻结或损坏，请检查传感器状态和环境温度'
        suggestion = '检查传感器是否被冻住、更换传感器或调整安装位置'
    elif -10 <= value < 0:
        reason = f'温度{value}℃：温度异常偏低，可能存在设备未启动或冷媒泄漏'
        suggestion = '检查设备运行状态、排查冷媒系统'
    elif value >= 80:
        reason = f'温度{value}℃：温度持续偏高，可能存在散热不良或工艺参数异常'
        suggestion = '检查散热系统、清理积灰、核对工艺设定值'
    elif value >= 70:
        reason = f'温度{value}℃：温度偏高，建议关注设备运行状态'
        suggestion = '观察设备运行、检查冷却系统'
    else:
        reason = f'温度{value}℃：偏离正常范围，建议检查设备或工艺参数'
        suggestion = '检查设备状态、核对工艺参数'

    # 添加触发规则信息
    if rule_type == '3sigma':
        rule_label = '3σ规则(极端异常)'
    elif rule_type == 'iqr':
        rule_label = 'IQR规则(偏态异常)'
    else:
        rule_label = '混合规则'

    return {
        'reason': f'{reason}(触发{rule_label})',
        'suggestion': suggestion
    }
for anomaly in anomalies:
    data_id, value, rule_type, params_str = anomaly
    params = json.loads(params_str) if params_str else {}
    
    # 根据数值重新判断实际规则类型
    def determine_rule_type(val):
        if val >= 80 or val <= -40:
            return '3sigma'
        elif -10 <= val < 0:
            return 'iqr'
        else:
            return '混合'
    
    actual_rule = determine_rule_type(value)
    result = generate_explanation(value, actual_rule)
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