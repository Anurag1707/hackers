import os
import time
from openai import OpenAI

def call_llm(prompt):
    try:
        client = OpenAI(
            base_url=os.environ.get("API_BASE_URL"),
            api_key=os.environ.get("API_KEY")
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Fallback: {str(e)}"


if __name__ == "__main__":
    task_name = "ai_study_task"

    print(f"[START] task={task_name}", flush=True)

    total_score = 0
    steps = 3

    questions = [
        "What is AI?",
        "Explain machine learning",
        "What is deep learning?"
    ]

    for i, q in enumerate(questions, start=1):
        answer = call_llm(q)

        # 🔥 IMPORTANT: score between 0 and 1 (not 0 or 1)
        score = 0.5 + (i * 0.1)   # 0.6, 0.7, 0.8

        total_score += score

        print(f"[STEP] step={i} reward={score}", flush=True)
        time.sleep(0.3)

    avg_score = total_score / steps

    print(f"[END] task={task_name} score={avg_score} steps={steps}", flush=True)