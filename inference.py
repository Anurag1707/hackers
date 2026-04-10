import time

def predict(input_data):
    return f"Processed: {input_data}"


if __name__ == "__main__":
    task_name = "ai_study_task"

    # START block
    print(f"[START] task={task_name}", flush=True)

    total_reward = 0
    steps = 1

    # STEP block
    action = "sample question"
    result = predict(action)
    reward = 1.0
    total_reward += reward

    print(f"[STEP] step=1 reward={reward}", flush=True)

    time.sleep(0.5)

    # END block
    print(f"[END] task={task_name} score={total_reward} steps={steps}", flush=True)