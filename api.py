from flask import Flask, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

@app.route('/')
def test():
    return 'Flask is running'

@app.route('/anomalies')
def get_anomalies():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='Root2024',
        database='tianqing_db',
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.timestamp, c.value, e.anomaly_reason 
        FROM cleaned_data c
        JOIN explanations e ON c.id = e.cleaned_data_id
        ORDER BY c.timestamp DESC 
        LIMIT 50
    """)
    rows = cursor.fetchall()
    conn.close()
    
    anomalies = [{'timestamp': str(r[0]), 'value': r[1], 'reason': r[2]} for r in rows]
    return jsonify(anomalies)

if __name__ == '__main__':
    app.run(port=5000)