from fastapi import FastAPI
import random

app = FastAPI()

env_state = {
    "step": 0,
    "score": 0
}

@app.post("/reset")
def reset():
    global env_state
    env_state = {
        "step": 0,
        "score": 0
    }
    return {"state": env_state}

@app.post("/step")
def step(action: dict):
    global env_state
    
    env_state["step"] += 1
    reward = random.randint(1, 10)
    env_state["score"] += reward

    done = env_state["step"] >= 10

    return {
        "state": env_state,
        "reward": reward,
        "done": done
    }

@app.get("/state")
def state():
    return env_state