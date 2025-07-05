from flask import Flask, request, session, render_template
from instagrapi import Client
import os, time, uuid
from threading import Thread
from itertools import cycle

app = Flask(__name__)
app.secret_key = 'yuvi-king-secret'

clients = {}
stop_flags = {}
msg_count = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ig-spammer', methods=['GET', 'POST'])
def ig_spammer():
HTML_HEAD = """
<!DOCTYPE html>
<html>
<head>
    <title>IG Tool by KING MAKER YUVI</title>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css' rel='stylesheet'>
    <style>
        body, html {
            height: 100%;
            margin: 0;
            font-family: Arial, sans-serif;
            color: white;
        }
        video.bg-video {
            position: fixed;
            top: 0;
            left: 0;
            min-width: 100%;
            min-height: 100%;
            object-fit: cover;
            z-index: -1;
            opacity: 0.3;
        }
        .container {
            background: rgba(0, 0, 0, 0.6);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 0 20px #ff69b4;
            margin-top: 30px;
        }
        .logo {
            height: 100px;
            border-radius: 20px;
            box-shadow: 0 0 20px #0ff;
        }
        h1, h2, h4, h5 {
            color: #99ffcc;
            text-shadow: 0 0 5px #ff69b4;
        }
        label {
            font-weight: bold;
            color: #ffffff;
        }
        input, select, textarea {
            margin-bottom: 10px;
            border: 2px solid #99ff99;
            background: rgba(255, 255, 255, 0.9);
            color: #000;
        }
        .btn-success {
            background-color: #ff66cc;
            border-color: #ff66cc;
            color: #fff;
            box-shadow: 0 0 10px #ff66cc;
        }
        .btn-danger {
            background-color: #ff1a75;
            border-color: #ff1a75;
            color: #fff;
            box-shadow: 0 0 10px #ff1a75;
        }
        .btn-success:hover, .btn-danger:hover {
            box-shadow: 0 0 20px #ff33aa;
        }
    </style>
</head>
<body>
    <video class="bg-video" autoplay muted loop>
        <source src="https://cdn.pixabay.com/video/2023/05/31/167252-829595670_large.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>

    <div class='text-center mt-3'>
        <img src='https://i.postimg.cc/Kcr5V75s/a58f941bc7aaad40797dfe63fcaaa34e.jpg' alt='KING MAKER YUVI' class='logo'>
        <h1>TOOL PANEL BY KING MAKER YUVI</h1>
    </div>
    <div class='container'>
        <h2 class='text-center'>👑 INSTAGRAM SPAMMER TOOL BY KING MAKER YUVI 👑</h2><hr>
"""

    HTML_FOOT = """
                <p class='text-center mt-4'>Made with ❤️ by <b>KING MAKER YUVI</b></p>
            </div>
        </div>
    </body>
    </html>
    """

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

        except Exception as e:
            return HTML_HEAD + f"<h4>❌ Login Error: {e}</h4><a href='/ig-spammer'>Back</a>" + HTML_FOOT

        thread_key = str(uuid.uuid4())[:8]

        def spam():
            stop_flags[thread_key] = False
            msg_count[thread_key] = 0
            try:
                if group_thread_id:
                    for msg in cycle(messages):
                        if stop_flags[thread_key]:
                            break
                        cl.direct_send(msg, thread_ids=[group_thread_id])
                        msg_count[thread_key] += 1
                        time.sleep(time_interval)
                elif target_username:
                    user_id = cl.user_id_from_username(target_username)
                    for msg in cycle(messages):
                        if stop_flags[thread_key]:
                            break
                        cl.direct_send(msg, [user_id])
                        msg_count[thread_key] += 1
                        time.sleep(time_interval)
            except Exception as e:
                print("Error in spam thread:", e)

        thread = Thread(target=spam)
        thread.start()
        clients[thread_key] = {"username": username, "client": cl, "thread": thread}
        session['username'] = username

        return HTML_HEAD + f"""
        <div class='text-center'>
        <div class='loader'></div>
        <h4 class='mt-3'>✅ Started attack for <b>{username}</b></h4>
        <h5>🚩 STOP Key: <code>{thread_key}</code></h5>
        <h4>📨 Messages Sent: <span id='count'>0</span></h4>
        <script>
        setInterval(() => {{
            fetch('/msg-count/{thread_key}').then(r => r.text()).then(txt => {{
                document.getElementById("count").innerText = txt;
            }});
        }}, 2000);
        </script>
        <a href='/ig-spammer'>Back</a></div>
        """ + HTML_FOOT

    html = HTML_HEAD + """
    <form method='post' enctype='multipart/form-data'>
        <label>Username:</label><input name='username' class='form-control' required>
        <label>Password:</label><input name='password' type='password' class='form-control' required>
        <label>Target Username:</label><input name='targetUsername' class='form-control'>
        <label>OR Group Thread ID:</label><input name='groupThreadId' class='form-control'>
        <label>Message File (.txt):</label><input type='file' name='txtFile' class='form-control' required>
        <label>Time Interval (seconds):</label><input type='number' name='timeInterval' class='form-control' value='2' required>
        <button type='submit' class='btn btn-success w-100 mt-3'>🚀 Launch Attack</button>
    </form>
    <hr>
    <form method='post' action='/stop'>
        <label>Enter STOP Key:</label><input name='thread_key' class='form-control' required>
        <button type='submit' class='btn btn-danger w-100 mt-2'>🚩 STOP</button>
    </form>
    """ + HTML_FOOT
    return html

@app.route('/stop', methods=['POST'])
def stop():
    thread_key = request.form['thread_key']
    if thread_key in stop_flags:
        stop_flags[thread_key] = True
        return f"<h3>🚩 Stopped key: {thread_key}</h3><a href='/ig-spammer'>Back</a>"
    return f"<h3>❌ Invalid key: {thread_key}</h3><a href='/ig-spammer'>Back</a>"

@app.route('/msg-count/<thread_key>')
def get_msg_count(thread_key):
    return str(msg_count.get(thread_key, 0))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
