from env.tasks import sample_task
from env.reward import compute_reward

class StudyEnv:
    def __init__(self, level="easy"):
        self.level = level
        self.state = None
        self.history = []

    def reset(self):
        task = sample_task(self.level)

        self.state = {
            "question": task["question"],
            "context": task["context"],
            "student_level": self.level,
            "history": []
        }

        return self.state

    def step(self, action, response):
        reward = compute_reward(response, self.state["context"])

        self.history.append({
            "action": action,
            "response": response,
            "reward": reward
        })

        self.state["history"] = self.history

        done = reward > 0.8

        return {
            "state": self.state,
            "reward": reward,
            "done": done
        }

    def get_state(self):
        return self.state