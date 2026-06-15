import pymysql
import numpy as np
from scipy.stats import skew

# 简化版缺失值填充（线性插值）
def simple_fill_missing(values):
    arr = np.array(values, dtype=float)
    mask = np.isnan(arr)
    if not mask.any():
        return arr.tolist()
    indices = np.arange(len(arr))
    arr[mask] = np.interp(indices[mask], indices[~mask], arr[~mask])
    return arr.tolist()

# 简化版标准化
def simple_normalize(values):
    arr = np.array(values, dtype=float)
    mean_val = np.mean(arr)
    std_val = np.std(arr)
    if std_val == 0:
        return arr.tolist()
    return ((arr - mean_val) / std_val).tolist()

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='Root2024',
    database='tianqing_db',
    charset='utf8mb4'
)
cursor = conn.cursor()

# 1. 读取规则
cursor.execute("SELECT id, rule_name, params FROM rules WHERE rule_name = '温度异常检测'")
rule = cursor.fetchone()
if rule is None:
    print("错误：没有找到规则")
    exit()
rule_id, rule_name, params_str = rule

# 2. 读取温度数据
cursor.execute("SELECT id, value FROM raw_data WHERE sensor_id = 'temperature' AND value IS NOT NULL")
rows = cursor.fetchall()
valid_values = [val for _, val in rows]

print(f"读取到 {len(rows)} 条数据")

# 缺失值填充 + 标准化
filled = simple_fill_missing(valid_values)
normalized = simple_normalize(filled)

if len(normalized) > 0:
    # 3. 计算偏度
    skewness = skew(normalized)
    print(f"数据偏度: {skewness:.2f}")
    
    if abs(skewness) > 0.5:
        print("数据偏态严重，使用 IQR 规则")
        q1 = np.percentile(normalized, 25)
        q3 = np.percentile(normalized, 75)
        iqr_val = q3 - q1
        lower_bound = q1 - 1.5 * iqr_val
        upper_bound = q3 + 1.5 * iqr_val
    else:
        print("数据近似正态，使用 3σ 规则")
        threshold = eval(params_str).get('threshold', 3)
        mean = np.mean(normalized)
        std = np.std(normalized)
        lower_bound = mean - threshold * std
        upper_bound = mean + threshold * std
        print(f"均值: {mean:.2f}, 标准差: {std:.2f}")
    
    print(f"正常范围: [{lower_bound:.2f}, {upper_bound:.2f}]")
    
    # 4. 检测异常并写入 cleaned_data
    for data_id, val in rows:
        # 原始值标准化
        orig_mean = np.mean(valid_values)
        orig_std = np.std(valid_values)
        norm_val = (val - orig_mean) / orig_std if orig_std > 0 else 0
        if norm_val < lower_bound or norm_val > upper_bound:
            print(f"发现异常: ID={data_id}, 值={val:.2f}")
            cursor.execute(
                "INSERT INTO cleaned_data (raw_data_id, timestamp, sensor_id, value, unit, rule_id, is_anomaly) "
                "VALUES (%s, NOW(), 'temperature', %s, '摄氏度', %s, 1)",
                (data_id, val, rule_id)
            )
        else:
            cursor.execute(
                "INSERT INTO cleaned_data (raw_data_id, timestamp, sensor_id, value, unit, rule_id, is_anomaly) "
                "VALUES (%s, NOW(), 'temperature', %s, '摄氏度', %s, 0)",
                (data_id, val, rule_id)
            )
    conn.commit()
    print(f"处理完成，共处理 {len(rows)} 条数据")

cursor.close()
conn.close()