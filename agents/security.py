def validate_input(user_input):

    blocked_words = [
        "ignore instructions",
        "show api key",
        "reveal system prompt"
    ]

    for word in blocked_words:
        if word.lower() in user_input.lower():
            return False

    return True