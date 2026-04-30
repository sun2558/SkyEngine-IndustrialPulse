import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)
n_rows = 1000
timestamps = [datetime(2025, 1, 1, 0, 0) + timedelta(minutes=10*i) for i in range(n_rows)]

# 偏态分布：大部分订单量小，少量订单量大
order_quantity = np.random.exponential(scale=2, size=n_rows).astype(int) + 1
order_quantity = np.clip(order_quantity, 1, 50)

df = pd.DataFrame({
    'timestamp': timestamps,
    'sensor_id': 'order_count',
    'value': order_quantity,
    'unit': '件'
})
df.to_csv('data/ecommerce_demo.csv', index=False)
print("电商数据生成完成，偏态分布")