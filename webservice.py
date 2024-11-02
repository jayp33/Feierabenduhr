from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route('/<sometext>', methods=['GET'])
def write_to_file(sometext):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('output.txt', 'a') as f:
        f.write(f'{timestamp} - {sometext}\n')
    return f'Text "{sometext}" with timestamp written to file.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
