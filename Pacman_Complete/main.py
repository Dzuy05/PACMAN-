# main.py
import subprocess

# Chạy run.py
run_process = subprocess.Popen(['python', 'run.py'])

# Chạy hand.py
hand_process = subprocess.Popen(['python', 'hand.py'])

# Chờ cho cả hai tiến trình kết thúc
run_process.wait()
hand_process.wait()