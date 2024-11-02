import http.client
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
        print("Fehler beim Lesen der Datei: {}".format(e))
        return None

def send_app_to_awtrix(app_name, text, icon, duration):
    headers = {"Content-Type": "application/json"}
    data = {
        "text": text,
        "icon": icon,
        "duration": duration,
        "lifetime": 600
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
        result = subprocess.run(['ping', '-c', '1', awtrix_ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=5)
        return result.returncode == 0

    except subprocess.TimeoutExpired:
        print("Timeout: {} is not reachable".format(awtrix_ip))
        return False

def main():
    while True:
        try:
            print("Checking host availability...")
            if host_available():
                print("Host is available. Reading task text...")
                task_text = get_tasktimer_text(file_path)
                if task_text:
                    print("Task text: {}".format(task_text))
                    send_app_to_awtrix("tasktimer", task_text, 7320, 600)
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
    main()

