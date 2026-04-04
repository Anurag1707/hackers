import random

def get_easy_task():
    return {
        "question": "What is Artificial Intelligence?",
        "context": "Artificial Intelligence (AI) is the ability of machines to perform tasks that typically require human intelligence."
    }

def get_medium_task():
    return {
        "question": "Summarize the following text",
        "context": "Artificial Intelligence is transforming industries by automating tasks, improving efficiency, and enabling data-driven decision making."
    }

def get_hard_task():
    return {
        "question": "Explain Machine Learning in simple terms",
        "context": "Machine Learning is a subset of AI that allows systems to learn and improve from experience without being explicitly programmed."
    }

def sample_task(level):
    if level == "easy":
        return get_easy_task()
    elif level == "medium":
        return get_medium_task()
    else:
        return get_hard_task()