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

cursor.execute("""
    SELECT c.id, c.value, r.rule_name, r.rule_type, r.params
    FROM cleaned_data c
    JOIN rules r ON c.rule_id = r.id
    WHERE c.is_anomaly = True
""")
anomalies = cursor.fetchall()

def generate_explanation(value, rule_type, params):
    if rule_type == '3sigma':
        mean = float(params.get('mean', 0))
        std = float(params.get('std', 1))
        lower = mean - 3 * std
        upper = mean + 3 * std
        return f"温度{value}℃超过正常范围（{lower:.2f}~{upper:.2f}℃),触发3σ异常检测"
    elif rule_type == 'iqr':
        q1 = float(params.get('q1', 0))
        q3 = float(params.get('q3', 1))
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        return f"温度{value}℃超过正常范围（{lower:.2f}~{upper:.2f}℃),触发IQR异常检测"
    return "异常触发"

for anomaly in anomalies:
    data_id, value, rule_name, rule_type, params_str = anomaly
    params = json.loads(params_str) if params_str else {}
    explanation = generate_explanation(value, rule_type, params)
    print(f"ID {data_id}: {explanation}")
    cursor.execute(
        "INSERT INTO explanations (cleaned_data_id, anomaly_reason) VALUES (%s, %s)",
        (data_id, explanation)
    )

conn.commit()
cursor.close()
conn.close()
print("完成")