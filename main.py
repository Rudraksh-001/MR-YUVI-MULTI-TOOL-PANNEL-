
from flask import Flask, render_template
import datetime
import requests
app = Flask(__name__)

@app.route('/')
def index():
    current_time = datetime.datetime.now()
    ip = get_ip()
    return render_template('index.html', time=current_time.strftime("%H:%M:%S"), date=current_time.strftime("%A, %d %B %Y"), ip=ip)

def get_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        return response.json().get("ip", "Unavailable")
    except:
        return "Unavailable"

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
