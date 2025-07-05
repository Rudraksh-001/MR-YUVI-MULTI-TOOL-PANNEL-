from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <html>
    <head>
        <title>👑 TOOL PANEL - KING MAKER YUVI 👑</title>
        <style>
            body {
                background: black;
                color: #00ff99;
                font-family: monospace;
                text-align: center;
                padding: 40px;
            }
            a {
                display: block;
                margin: 15px;
                font-size: 20px;
                color: cyan;
                text-decoration: none;
            }
            a:hover {
                color: magenta;
                text-shadow: 0 0 10px magenta;
            }
            .logo {
                font-size: 30px;
                font-weight: bold;
                text-shadow: 0 0 10px #0f0;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="logo">👑 KING MAKER YUVI PANEL 👑</div>
        <hr>
        <a href="/fb-token-checker">🔥 Facebook Token Checker</a>
        <a href="/ig-spammer">📸 Instagram Spammer Tool</a>
        <a href="/group-uid">👥 Group UID Extractor</a>
        <a href="/whatsapp-sender">📞 WhatsApp Sender Tool</a>
        <hr>
        <div>Made by LEGEND YUVI INSIDE 💚</div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
