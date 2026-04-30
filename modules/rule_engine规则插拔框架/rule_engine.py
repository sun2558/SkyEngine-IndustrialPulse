import pymysql
import numpy as np
from scipy.stats import skew, iqr  # 新增导入

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='Root2024',
    database='tianqing_db',
    charset='utf8mb4'
)
cursor = conn.cursor()

# 1. 读取规则（先只读温度规则，演示自动切换）
cursor.execute("SELECT rule_name, params FROM rules WHERE rule_type = '3sigma'")
rule = cursor.fetchone()
rule_name, params_str = rule

# 2. 读取温度数据
cursor.execute("SELECT id, value FROM raw_data WHERE sensor_id = 'temperature' AND value IS NOT NULL")
rows = cursor.fetchall()
valid_values = [val for _, val in rows]

if valid_values:
    # 3. 计算偏度，决定用三西格玛还是IQR
    skewness = skew(valid_values)
    print(f"数据偏度: {skewness:.2f}")
    
    if abs(skewness) > 0.5:
        print("数据偏态严重，使用 IQR 规则")
        # IQR 逻辑
        q1 = np.percentile(valid_values, 25)
        q3 = np.percentile(valid_values, 75)
        iqr_val = q3 - q1
        lower_bound = q1 - 1.5 * iqr_val
        upper_bound = q3 + 1.5 * iqr_val
    else:
        print("数据近似正态，使用 3σ 规则")
        threshold = eval(params_str).get('threshold', 3)
        mean = np.mean(valid_values)
        std = np.std(valid_values)
        lower_bound = mean - threshold * std
        upper_bound = mean + threshold * std
        print(f"均值: {mean:.2f}, 标准差: {std:.2f}")
    
    print(f"正常范围: [{lower_bound:.2f}, {upper_bound:.2f}]")
    
    # 4. 检测异常（逻辑不变）
    for data_id, val in rows:
        if val < lower_bound or val > upper_bound:
            print(f"发现异常: ID={data_id}, 值={val:.2f}")