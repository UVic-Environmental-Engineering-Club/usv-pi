def parse_string(message: str) -> str:

    split_message = message.split("-")
    type = split_message.pop(0)

    return {"type": type, "data": split_message}
