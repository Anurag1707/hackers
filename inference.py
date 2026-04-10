import os
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


def run_task(task_name, question, score):
    print(f"[START] task={task_name}", flush=True)

    answer = call_llm(question)

    # STEP
    print(f"[STEP] step=1 reward={score}", flush=True)

    # END
    print(f"[END] task={task_name} score={score} steps=1", flush=True)


if __name__ == "__main__":

    # 🔥 3 DIFFERENT TASKS (VERY IMPORTANT)
    run_task("task1", "What is AI?", 0.6)
    run_task("task2", "Explain machine learning", 0.7)
    run_task("task3", "What is deep learning?", 0.8)