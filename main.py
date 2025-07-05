from flask import Flask, request, session, render_template
from instagrapi import Client
import os
import time
import uuid
from threading import Thread

app = Flask(__name__)
app.secret_key = 'yuvi-king-secret'

clients = {}
stop_flags = {}

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

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
