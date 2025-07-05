from flask import Flask, render_template
from datetime import datetime
import requests

app = Flask(__name__)

def get_ip():
    try:
        res = requests.get("https://api.ipify.org?format=json", timeout=3)
        return res.json().get("ip", "Unavailable")
    except:
        return "Unavailable"

@app.route('/')
def panel():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d-%m-%Y")
    ip = get_ip()
    return render_template("index.html", time=current_time, date=current_date, ip=ip)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
