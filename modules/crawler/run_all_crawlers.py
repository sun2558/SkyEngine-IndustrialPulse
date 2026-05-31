import subprocess
import os

scripts = ['crawler_weather.py', 'crawler_ecommerce.py', 'crawler_factory.py']
for script in scripts:
    print(f"运行 {script}...")
    subprocess.run(['python', os.path.join(os.path.dirname(__file__), script)])