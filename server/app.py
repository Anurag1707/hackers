from flask import Flask, request, jsonify

app = Flask(__name__)

state = {"observation": ""}

@app.route("/reset", methods=["POST"])
def reset():
    global state
    state["observation"] = "reset done"
    return jsonify({"observation": state["observation"]})

@app.route("/step", methods=["POST"])
def step():
    global state
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

@app.route("/")
def home():
    return "OpenEnv Running ✅"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)