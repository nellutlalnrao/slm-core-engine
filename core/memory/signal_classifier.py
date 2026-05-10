def tag_message(text: str):
    tags = []

    if "?" in text:
        tags.append("question")

    if "code" in text or "python" in text:
        tags.append("code_request")

    return tags