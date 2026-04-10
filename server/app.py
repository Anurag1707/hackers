from flask import Flask, request, jsonify

def create_app():
    app = Flask(__name__)
    state = {"observation": ""}

    @app.route("/")
    def home():
        return """
        <html>
        <head>
            <title>AI Study Assistant - OpenEnv</title>
            <style>
                body {
                    font-family: 'Segoe UI', Arial;
                    background: linear-gradient(135deg, #e0f2fe, #f8fafc);
                    text-align: center;
                    padding: 40px;
                }
                .container {
                    background: white;
                    padding: 30px;
                    border-radius: 15px;
                    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
                    display: inline-block;
                    max-width: 500px;
                }
                h1 {
                    color: #1e3a8a;
                }
                .status {
                    color: green;
                    font-weight: bold;
                }
                .btn {
                    display: inline-block;
                    margin-top: 15px;
                    padding: 12px 20px;
                    background: #2563eb;
                    color: white;
                    text-decoration: none;
                    border-radius: 10px;
                    font-weight: bold;
                }
                .btn:hover {
                    background: #1d4ed8;
                }
                ul {
                    text-align: left;
                    margin-top: 15px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎓 AI Study Assistant</h1>
                <p class="status">✅ OpenEnv Server Running</p>
                <h3>📌 Project Features:</h3>
                <ul>
                    <li>AI Question Answering</li>
                    <li>Voice Assistant</li>
                    <li>PDF & Notes Summarizer</li>
                    <li>Smart Search System</li>
                </ul>
                <h3>🎯 API Endpoints:</h3>
                <p>/reset | /step | /state</p>
                <h3>🚀 Live Demo:</h3>
                <a class="btn" href="https://Anurag9424-AuraAI.hf.space" target="_blank">
                    Open Streamlit App
                </a>
                <p style="margin-top:20px; font-size: 14px; color: gray;">
                    Powered by OpenEnv | Hackathon Project
                </p>
            </div>
        </body>
        </html>
        """

    @app.route("/reset", methods=["POST"])
    def reset():
        state["observation"] = "Environment reset successful"
        return jsonify({"observation": state["observation"]})

    @app.route("/step", methods=["POST"])
    def step():
        data = request.json
        action = data.get("action", "")

        observation = f"Processed: {action}"
        state["observation"] = observation

        return jsonify({
            "observation": observation,
            "reward": 1,
            "done": False,
            "info": {}
        })

    @app.route("/state", methods=["GET"])
    def get_state():
        return jsonify(state)

    return app


def main():
    app = create_app()
    app.run(host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()