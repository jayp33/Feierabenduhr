import http.client
import time
import socket
import json
import argparse
import os
import re
from datetime import datetime, timedelta

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load configuration from file in the script directory
config_path = os.path.join(script_dir, 'config.json')
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

awtrix_ip = config['awtrix_ip']
work_duration = config['WorkDuration']
task_timer_work_duration = config['TaskTimerWorkDuration']
over_time_minutes = task_timer_work_duration - work_duration

def get_tasktimer_text(file_path):
    try:
        with open(file_path, 'r') as file:
            first_line = file.readline().strip()
            first_word = first_line.split()[0]
            return first_word.lstrip('\ufeff')  # Remove BOM if present
    except Exception as e:
        print("Fehler beim Lesen der Datei: {}".format(e))
        return None

def is_valid_time_format(task_text: str) -> bool:
    pattern = r'^\d{2}:\d{2}$'
    return bool(re.match(pattern, task_text))

def calculate_closing_time(task_time, task_timer_work_duration, work_duration):
    """
    Berechnet den Feierabend basierend auf der Anzeige im Task Timer und der eingestellten Überstunden.

    :param task_time: Die vom Task Timer angezeigte Feierabend Uhrzeit (datetime.time).
    :param task_timer_work_duration: Die im Task Timer eingestellte Arbeitsdauer in Minuten (int).
    :param work_duration: Die reguläre Arbeitsdauer in Minuten (int).
    :return: Die reguläre Feierabend Uhrzeit (datetime.time).
    """
    overtime = task_timer_work_duration - work_duration
    closing_time = (datetime.combine(datetime.today(), task_time) - timedelta(minutes=overtime)).time()
    return closing_time

def send_app_to_awtrix(app_name, text, icon, duration, color):
    headers = {"Content-Type": "application/json"}
    data = {
        "text": text,
        "icon": icon,
        "duration": duration,
        "lifetime": 3600,
        "color": color
    }

    awtrix_url = "/api/custom?name=" + app_name
    conn = http.client.HTTPConnection(awtrix_ip)
    conn.request("POST", awtrix_url, body=json.dumps(data), headers=headers)
    response = conn.getresponse()
    
    if response.read().decode() != "OK":
        print(response.read().decode())
    conn.close()

    # time.sleep(duration * 4)

def host_available():
    try:
        # Attempt to connect to the host on port 80 (HTTP)
        with socket.create_connection((awtrix_ip, 80), timeout=5):
            return True
    except (socket.timeout, socket.error) as e:
        print("Error: {} is not reachable. Exception: {}".format(awtrix_ip, e))
        return False

def main(file_path):
    while True:
        try:
            print("Checking host availability...")
            if host_available():
                print("Host is available. Reading task text...")
                task_text = get_tasktimer_text(file_path)
                if is_valid_time_format(task_text):
                    print("Task text: {}".format(task_text))
                    try:
                        task_time = datetime.strptime(task_text, "%H:%M").time()
                        print("task_time: {}".format(task_time))
                        closing_time = calculate_closing_time(task_time, task_timer_work_duration, work_duration)
                        print("Feierabend: {}".format(closing_time))

                        current_time = datetime.now().time()
                        if closing_time <= current_time:
                            color = "#00ff00"  # Green
                            # Calculate the time passed since the official closing time
                            time_passed = datetime.combine(datetime.today(), current_time) - datetime.combine(datetime.today(), closing_time)
                            task_text = "{:01}:{:02}".format(time_passed.seconds // 3600, (time_passed.seconds // 60) % 60)
                            print("Updated task text: {}".format(task_text))
                        else:
                            color = "#ffffff"  # White
                    except ValueError as ve:
                        print("ValueError: {}".format(ve))
                        color = "#ffffff"  # White if not in HH:mm format
                    send_app_to_awtrix("tasktimer", task_text, 7320, 600, color)
                else:
                    print("No task text found.")
            else:
                print("Host is not available.")
            
            print("Sleeping for 30 seconds...")
            time.sleep(30)
        except Exception as e:
            print("Fehler: {}".format(e))
            print("Sleeping for 60 seconds due to error...")
            time.sleep(60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the task timer script with a specified file path.')
    parser.add_argument('file_path', type=str, help='The path to the file containing the task text.')
    args = parser.parse_args()
    main(args.file_path)
