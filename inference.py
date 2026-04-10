import os
from openai import OpenAI

def call_llm(prompt):
    client = OpenAI(
        base_url=os.environ["API_BASE_URL"],  # 🔥 MUST
        api_key=os.environ["API_KEY"]         # 🔥 MUST
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    task_name = "ai_study_task"

    # START
    print(f"[START] task={task_name}", flush=True)

    total_reward = 0
    steps = 1

    # STEP (LLM CALL 🔥)
    question = "What is machine learning?"
    answer = call_llm(question)

    reward = 1.0
    total_reward += reward

    print(f"[STEP] step=1 reward={reward}", flush=True)

    # END
    print(f"[END] task={task_name} score={total_reward} steps={steps}", flush=True)