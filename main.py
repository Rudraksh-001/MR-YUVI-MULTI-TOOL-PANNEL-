from flask import Flask, render_template, jsonify
from datetime import datetime
import requests
from instagrapi import Client
import os
import time
import uuid
from threading import Thread

app = Flask(__name__)
app.secret_key = 'yuvi-king-secret'

clients = {}
stop_flags = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/live-info")
def live_info():
    now = datetime.now()
    return jsonify({
        "time": now.strftime("%H:%M:%S"),
        "date": now.strftime("%Y-%m-%d"),
        "ip": requests.get('https://api.ipify.org').text
    })
    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ig-spammer', methods=['GET', 'POST'])
def ig_spammer():
    HTML_TEMPLATE_HEAD = """<!DOCTYPE html>
<html><head><meta charset='utf-8'><title>IG TOOL</title><style>
body { background:#000; color:#00ff99; font-family:monospace; padding:40px; }
input,button { padding:10px; width:100%%; margin-bottom:10px; }
</style></head><body><h2>Instagram Spammer - KING MAKER YUVI</h2>"""
    HTML_TEMPLATE_FOOT = """</body></html>"""

    def send_messages(thread_key, cl, username, target_username, group_thread_id, messages, time_interval):
        stop_flags[thread_key] = False
        try:
            if group_thread_id:
                for i, msg in enumerate(messages, 1):
                    if stop_flags.get(thread_key): break
                    cl.direct_send(msg, thread_ids=[group_thread_id])
                    time.sleep(time_interval)
            elif target_username:
                user_id = cl.user_id_from_username(target_username)
                for i, msg in enumerate(messages, 1):
                    if stop_flags.get(thread_key): break
                    cl.direct_send(msg, [user_id])
                    time.sleep(time_interval)
        except Exception as e:
            print(f"[ERROR] {username} - {str(e)}")

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        target_username = request.form.get('targetUsername')
        group_thread_id = request.form.get('groupThreadId')
        time_interval = int(request.form['timeInterval'])
        txt_file = request.files['txtFile']

        file_path = os.path.join('/tmp', f'{username}_msgs.txt')
        txt_file.save(file_path)

        with open(file_path, 'r') as f:
            messages = f.read().splitlines()

        try:
            cl = Client()
            session_file = f"{username}_session.json"

            if os.path.exists(session_file):
                cl.load_settings(session_file)
                cl.login(username, password)
            else:
                cl.login(username, password)
                cl.dump_settings(session_file)

            thread_key = str(uuid.uuid4())[:8]
            thread = Thread(target=send_messages, args=(thread_key, cl, username, target_username, group_thread_id, messages, time_interval))
            thread.start()

            clients[thread_key] = { "username": username, "client": cl, "thread": thread }
            session['username'] = username

            return f"<h3>✅ Spam started for <b>{username}</b></h3><h5>STOP Key: <code>{thread_key}</code></h5><a href='/ig-spammer'>Back</a>"

        except Exception as e:
            return f"<h3>❌ Error: {e}</h3><a href='/ig-spammer'>Back</a>"

    active_keys_html = ""
    session_username = session.get('username')
    if session_username:
        user_keys = [k for k, v in clients.items() if v['username'] == session_username]
        if user_keys:
            active_keys_html += "<p>Your Active Thread Key(s):<br><textarea rows='3' readonly>"
            for key in user_keys:
                active_keys_html += f"{key}\n"
            active_keys_html += "</textarea></p>"

    html = HTML_TEMPLATE_HEAD + f"""
    <form method='post' enctype='multipart/form-data'>
      <input type='text' name='username' placeholder='Instagram Username' required>
      <input type='password' name='password' placeholder='Instagram Password' required>
      <input type='text' name='targetUsername' placeholder='Target Username (optional)'>
      <input type='text' name='groupThreadId' placeholder='Group Thread ID (optional)'>
      <input type='file' name='txtFile' accept='.txt' required>
      <input type='number' name='timeInterval' value='2' placeholder='Time Interval (sec)' required>
      <button type='submit'>🚀 Launch Attack</button>
    </form>
    <form method='post' action='/stop'>
      <input type='text' name='thread_key' placeholder='Enter STOP Key' required>
      <button type='submit'>🛑 Stop Messages</button>
    </form>
    """ + active_keys_html + HTML_TEMPLATE_FOOT
    return html

@app.route('/stop', methods=['POST'])
def stop_messages():
    thread_key = request.form['thread_key']
    if thread_key in stop_flags:
        stop_flags[thread_key] = True
        return f"<h3>🛑 Stopped thread: <code>{thread_key}</code></h3><a href='/ig-spammer'>Back</a>"
    return f"<h3>❌ Invalid key: <code>{thread_key}</code></h3><a href='/ig-spammer'>Back</a>"

@app.route('/token_checker', methods=['GET', 'POST'])
def token_checker():
    GRAPH_API_URL = "https://graph.facebook.com/v18.0"
    HTML_TEMPLATE = """ 
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FACEBOOK TOKEN CHECKER</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                background: url('https://i.ibb.co/wN84B8d8/IMG-20250628-WA0473.jpg') no-repeat center center fixed;
                background-size: cover;
                color: white;
                margin: 0;
                padding: 0;
            }
            .container {
                width: 90%;
                max-width: 400px;
                margin: 100px auto;
                padding: 20px;
                background: rgba(0, 0, 0, 0.7);
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(255, 255, 255, 0.3);
            }
            h2 {
                margin-bottom: 20px;
                font-size: 22px;
                text-transform: uppercase;
            }
            input {
                width: 90%;
                padding: 10px;
                margin: 10px 0;
                border: none;
                background: black;
                color: white;
                border-radius: 5px;
                text-align: center;
            }
            button {
                width: 95%;
                padding: 10px;
                background: blue;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                margin-top: 10px;
            }
            button:hover {
                background: darkblue;
            }
            .result {
                margin-top: 20px;
                padding: 10px;
                background: black;
                border-radius: 5px;
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>FACEBOOK UID CHECKER</h2>
            <form method="POST">
                <input type="text" name="token" placeholder="ENTER TOKEN" required>
                <button type="submit">CHECK TOKEN</button>
            </form>
            {% if groups %}
                <div class="result">
                    <h3>Messenger Groups:</h3>
                    <ul>
                        {% for group in groups %}
                            <li><strong>{{ group.name if group.name else 'Unnamed Group' }}</strong> - UID: {{ group.id }}</li>
                        {% endfor %}
                    </ul>
                </div>
            {% endif %}
            {% if error %}
                <p class="result" style="color: red;">{{ error }}</p>
            {% endif %}
            <div class="result">LEGEND YUVI INSIDE</div>
        </div>
    </body>
    </html>
    """

@app.route('/page-token', methods=['GET', 'POST'])
def page_token_tool():
    HTML_TEMPLATE = """ 
    <!-- HTML_TEMPLATE same as before --> 
    """
    pages = []
    error = None
    if request.method == 'POST':
        token = request.form.get('access_token')
        try:
            res = requests.get(f'https://graph.facebook.com/me/accounts?access_token={token}')
            data = res.json()
            if 'error' in data:
                error = data['error']['message']
            else:
                for page in data.get('data', []):
                    pages.append({
                        'name': page.get('name'),
                        'id': page.get('id'),
                        'token': page.get('access_token')
                    })
                if not pages:
                    error = "No pages found for this token."
        except Exception as e:
            error = "Error: " + str(e)
    return render_template_string(HTML_TEMPLATE, pages=pages, error=error)
    
    if request.method == 'POST':
        access_token = request.form.get('token')
        if not access_token:
            return render_template_string(HTML_TEMPLATE, error="Token is required")

        url = f"{GRAPH_API_URL}/me/conversations?fields=id,name&access_token={access_token}"
        try:
            response = requests.get(url)
            data = response.json()
            if "data" in data:
                return render_template_string(HTML_TEMPLATE, groups=data["data"])
            else:
                return render_template_string(HTML_TEMPLATE, error="Invalid token or no Messenger groups found")
        except:
            return render_template_string(HTML_TEMPLATE, error="Something went wrong")

    return render_template_string(HTML_TEMPLATE)
    
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
            
