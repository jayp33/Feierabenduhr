import requests
import time
import subprocess
import json

# Load configuration from file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

awtrix_ip = config['awtrix_ip']
file_path = config['file_path']

def get_tasktimer_text(file_path):
    try:
        with open(file_path, 'r') as file:
            first_line = file.readline().strip()
            first_word = first_line.split()[0]
            return first_word
    except Exception as e:
        print(f"Fehler beim Lesen der Datei: {e}")
        return None

def send_app_to_awtrix(app_name, text, icon, duration):
    headers = {"Content-Type": "application/json"}
    data = {
        "text": text,
        "icon": icon,
        "duration": duration,
        "lifetime": 600
    }

    awtrix_url = "http://"+ awtrix_ip + "/api/custom?name=" + app_name
    response = requests.post(awtrix_url, json=data, headers=headers)
    
    if response.text != "OK":
        print(response.text)

    # time.sleep(duration * 4)

def host_available():
    try:
        result = subprocess.run(['ping', '-c', '1', awtrix_ip], capture_output=True, text=True, timeout=5)
        return result.returncode == 0

    except subprocess.TimeoutExpired:
        print(f"Timeout: {awtrix_ip} is not reachable")
        return False

def main():
    while True:
        try:
            print("Checking host availability...")
            if host_available():
                print("Host is available. Reading task text...")
                task_text = get_tasktimer_text(file_path)
                if task_text:
                    print(f"Task text: {task_text}")
                    send_app_to_awtrix("tasktimer", task_text, 7320, 600)
                else:
                    print("No task text found.")
            else:
                print("Host is not available.")
            
            print("Sleeping for 30 seconds...")
            time.sleep(30)
        except Exception as e:
            print(f"Fehler: {e}")
            print("Sleeping for 60 seconds due to error...")
            time.sleep(60)

if __name__ == "__main__":
    main()

