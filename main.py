from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

GRAPH_API_URL = "https://graph.facebook.com/v18.0"

# HTML & CSS Template
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

@app.route('/', methods=['GET', 'POST'])
def home():
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
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, error="Something went wrong")

    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    print("🔥 Flask server started on port 5000...")
    app.run(host="0.0.0.0", port=5000, debug=True)
