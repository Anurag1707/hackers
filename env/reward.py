def compute_reward(response, context):
    score = 0.0

    # Length check (clarity)
    if len(response.split()) > 10:
        score += 0.3

    # Keyword match (correctness)
    context_words = context.lower().split()
    match_count = sum(1 for word in response.lower().split() if word in context_words)

    if match_count > 3:
        score += 0.4

    # Example bonus
    if "example" in response.lower():
        score += 0.3

    return min(score, 1.0)