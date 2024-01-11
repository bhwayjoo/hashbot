
# main_program.py
import subprocess
import threading
import time

def run_script(script_name):
    subprocess.run(["python", script_name])

def run_flask_app():
    subprocess.run(["python", "telegram_bot.py"])

if __name__ == "__main__":
    # Start script1.py in a separate thread
    thread_script1 = threading.Thread(target=run_script, args=("app4.py",))
    thread_script1.start()

    # Start script2.py in a separate thread
    thread_script2 = threading.Thread(target=run_script, args=("bot4.py",))
    thread_script2.start()

    # Start Flask app in the main thread
    run_flask_app()
