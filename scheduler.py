import schedule
import time
import subprocess

def run_rule_engine():
    print("[调度] 运行规则引擎...")
    subprocess.run(["python", "modules/rule_engine/rule_engine.py"])

def run_explain():
    print("[调度] 运行可解释AI...")
    subprocess.run(["python", "modules/xai_interface/explain_anomaly.py"])

# 每5分钟跑一次规则引擎
schedule.every(5).minutes.do(run_rule_engine)
# 规则引擎跑完后，再跑可解释AI（每5分钟跑一次）
schedule.every(5).minutes.do(run_explain)

print("调度器启动,每5分钟执行一次检测循环...")

while True:
    schedule.run_pending()
    time.sleep(1)