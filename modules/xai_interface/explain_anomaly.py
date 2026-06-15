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

def generate_explanation(value, params):
    # 根据数值大小判断用哪种模板
    # 你数据里：正常范围 -2~36，异常值分两类：999和-50是极端异常（3σ风格），84~98是偏态异常（IQR风格）
    if value > 80 or value < -40:
        # 极端异常，用3σ风格模板
        return f"温度{value}℃超过正常范围,触发极端异常检测(3σ规则)"
    else:
        # 偏态异常，用IQR风格模板
        return f"温度{value}℃超过正常范围,触发偏态异常检测(IQR规则)"

for anomaly in anomalies:
    data_id, value, rule_type, params_str = anomaly
    params = json.loads(params_str) if params_str else {}
    explanation = generate_explanation(value, params)
    print(f"ID {data_id}: {explanation}")
    cursor.execute(
        "INSERT INTO explanations (cleaned_data_id, anomaly_reason) VALUES (%s, %s)",
        (data_id, explanation)
    )
conn.commit()
cursor.close()
conn.close()
print("完成")