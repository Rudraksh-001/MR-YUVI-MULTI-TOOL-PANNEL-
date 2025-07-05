from flask import Flask, render_template_string

app = Flask(__name__)

HTML_PANEL = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>KING MAKER YUVI PANEL</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css');

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: 'Orbitron', sans-serif;
      display: flex;
      min-height: 100vh;
      background: linear-gradient(120deg, #1e1e2f, #3a1f47, #1b1b1b);
      color: white;
      overflow-x: hidden;
    }

    .sidebar {
      width: 240px;
      background-color: #111;
      padding: 30px 20px;
      display: flex;
      flex-direction: column;
      box-shadow: 5px 0 20px #00000080;
    }

    .sidebar h2 {
      color: #ff00cc;
      font-size: 24px;
      margin-bottom: 30px;
      text-align: center;
      text-shadow: 0 0 10px #ff00cc;
    }

    .sidebar a {
      color: white;
      text-decoration: none;
      margin: 10px 0;
      font-size: 16px;
      padding: 10px 15px;
      border-radius: 10px;
      transition: 0.3s;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .sidebar a:hover {
      background-color: #ff00cc44;
    }

    .main {
      flex: 1;
      padding: 30px;
    }

    .topnav {
      background: #222;
      padding: 10px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 4px 12px #00000080;
      margin-bottom: 30px;
    }

    .topnav h1 {
      font-size: 22px;
      color: #ff8cf5;
    }

    .welcome {
      font-size: 36px;
      text-align: center;
      margin-bottom: 25px;
      color: #ff6bf2;
      text-shadow: 0 0 15px #f09;
    }

    .info-box {
      display: flex;
      justify-content: space-between;
      padding: 18px;
      background: #ffffff12;
      border-radius: 12px;
      margin-bottom: 10px;
      box-shadow: 0 0 10px #ff00cc55;
    }

    .info-label { color: #ffc107; }
    .info-value { color: #00ffcc; }

    .tool-box {
      background: linear-gradient(145deg, #2a2a40, #202035);
      padding: 40px 30px;
      border-radius: 20px;
      margin: 30px 0;
      box-shadow: 0 0 25px #c38aff90;
      position: relative;
    }

    .tool-title {
      font-size: 26px;
      color: #ffaaff;
      margin-bottom: 15px;
      text-shadow: 0 0 12px #ffb3ff;
    }

    .tool-desc {
      font-size: 18px;
      color: #eee;
    }

    .open-tool-btn {
      margin-top: 20px;
      padding: 8px 20px;
      font-size: 13px;
      font-weight: bold;
      border: none;
      border-radius: 20px;
      background: linear-gradient(135deg, #ff5fe0, #b04fff);
      color: #fff;
      cursor: pointer;
      box-shadow: 0 0 12px #ff82ee;
      transition: 0.3s ease;
    }

    .open-tool-btn:hover {
      background: linear-gradient(135deg, #ffa0fc, #a56cff);
    }

    .logo {
      text-align: center;
      margin-bottom: 20px;
    }

    .logo img {
      max-width: 150px;
      border-radius: 20px;
      box-shadow: 0 0 20px #ff00ccaa;
    }

    @media(max-width: 768px) {
      .sidebar { display: none; }
      .main { padding: 20px; }
      .topnav h1 { font-size: 18px; }
      .welcome { font-size: 28px; }
      .tool-box { padding: 30px 20px; }
    }
  </style>
</head>
<body>
  <div class="sidebar">
    <div class="logo">
      <img src="https://i.postimg.cc/Kcr5V75s/a58f941bc7aaad40797dfe63fcaaa34e.jpg" alt="KING MAKER YUVI">
    </div>
    <h2><i class="fas fa-toolbox"></i> TOOLS</h2>
    <a href="#"><i class="fas fa-home"></i> Home</a>
    <a href="#"><i class="fas fa-wrench"></i> All Tools</a>
    <a href="#"><i class="fas fa-info-circle"></i> About</a>
    <a href="#"><i class="fas fa-envelope"></i> Contact</a>
  </div>

  <div class="main">
    <div class="topnav">
      <h1>🔥 KING MAKER YUVI TOOL PANEL</h1>
      <div><i class="fas fa-user-shield"></i> Admin</div>
    </div>

    <div class="welcome">🚀 Welcome LEGEND YUVI INSIDE 🚀</div>

    <div class="info-box"><span class="info-label">PING</span><span class="info-value">285 ms</span></div>
    <div class="info-box"><span class="info-label">TIME</span><span class="info-value" id="time">--:--:--</span></div>
    <div class="info-box"><span class="info-label">DATE</span><span class="info-value" id="date">--/--/----</span></div>
    <div class="info-box"><span class="info-label">IP</span><span class="info-value" id="ip">Loading...</span></div>

    {% for tool in tools %}
    <div class="tool-box">
      <div class="tool-title">{{ tool.title }}</div>
      <div class="tool-desc">{{ tool.desc }}</div>
      <button class="open-tool-btn" data-link="{{ tool.link }}">Open Tool</button>
    </div>
    {% endfor %}
  </div>

  <script>
    function updateTime() {
      const now = new Date();
      document.getElementById('time').textContent = now.toLocaleTimeString();
      document.getElementById('date').textContent = now.toDateString();
    }
    setInterval(updateTime, 1000);
    updateTime();

    fetch("https://api.ipify.org?format=json")
      .then(res => res.json())
      .then(data => {
        document.getElementById("ip").textContent = data.ip;
      });

    document.querySelectorAll('.open-tool-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const url = btn.getAttribute('data-link');
        if (url) window.open(url, '_blank');
      });
    });
  </script>
</body>
</html>
"""

@app.route('/')
def panel():
    tools = [
        {"title": "FB CONVO TOKEN SERVER", "desc": "Send messages to groups using tokens.", "link": "https://example.com/convo"},
        {"title": "FB AUTO COMMENT BOT", "desc": "Automatically comment on posts.", "link": "https://example.com/comment"},
        {"title": "FB GROUP POSTER", "desc": "Post to multiple groups with control.", "link": "https://example.com/poster"},
        {"title": "PAGE AUTO LIKER", "desc": "Increase page likes using tokens.", "link": "https://example.com/liker"},
        {"title": "UID SCANNER TOOL", "desc": "Scan group/page for UIDs fast.", "link": "https://example.com/scanner"},
        {"title": "FB TOKEN CHECKER", "desc": "Verify if token is valid & active.", "link": "https://example.com/checker"},
    ]
    return render_template_string(HTML_PANEL, tools=tools)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
