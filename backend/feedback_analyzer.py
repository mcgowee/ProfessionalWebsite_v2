def analyze_response(user_message):
    """
    Analyze user response and provide feedback.
    """
    if "calm" in user_message or "boundaries" in user_message:
        return "Good job! You maintained composure and set boundaries."
    elif "guilt" in user_message:
        return "Try to avoid letting guilt dictate your response. Stay assertive."
    else:
        return "Consider responding calmly and addressing the manipulator's intention without escalating."
