from flask import Flask, request, jsonify

app = Flask(__name__)


STREAMLIT_LINK = "https://Anurag9424-AuraAI.hf.space"

# Global state
state_data = {}


@app.route("/")
def home():
    return f"""
    <html>
    <head>
        <title>OpenEnv AI Study Assistant</title>
        <style>
            body {{
                font-family: Arial;
                text-align: center;
                padding: 40px;
                background-color: #f8fafc;
            }}
            h1 {{ color: #1e3a8a; }}
            a {{
                color: #2563eb;
                font-size: 20px;
                text-decoration: none;
                font-weight: bold;
            }}
            .box {{
                background: white;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                display: inline-block;
            }}
        </style>
    </head>
    <body>
        <div class="box">
            <h1>🚀 OpenEnv Running</h1>
            <p><b>Status:</b> ✅ Active</p>
            <h3>📌 Project Info:</h3>
            <p>AI Study Assistant Backend (OpenEnv API)</p>
            <h3>🎓 Live Demo:</h3>
            <a href="{STREAMLIT_LINK}" target="_blank">
                👉 Open Streamlit App
            </a>
            <br><br>
            <p>Use /reset, /step, /state APIs</p>
        </div>
    </body>
    </html>
    """


@app.route("/reset", methods=["POST"])
def reset():
    global state_data
    state_data = {
        "message": "Environment reset successful",
        "demo_app": STREAMLIT_LINK
    }
    return jsonify(state_data)

# STEP
@app.route("/step", methods=["POST"])
def step():
    global state_data
    data = request.json

    action = data.get("action", "")

    # Simple AI logic
    answer = f"AI Answer for: {action}"

    state_data = {
        "question": action,
        "answer": answer,
        "demo_app": STREAMLIT_LINK
    }

    return jsonify({
        "state": state_data,
        "reward": 1,
        "done": False
    })

# STATE
@app.route("/state", methods=["GET"])
def state():
    return jsonify({
        "current_state": state_data,
        "demo_app": STREAMLIT_LINK,
        "info": "Full UI available in Streamlit app",
        "features": [
            "Voice Assistant",
            "PDF Summarizer",
            "Smart Search",
            "Notes Generator"
        ]
    })

# RUN SERVER
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)