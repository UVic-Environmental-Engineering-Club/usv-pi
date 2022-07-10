import json
from typing import Dict


def parse_string(message: str) -> Dict[str, float]:
    if message is not None:
        split_message = message.split(":")
        message_type = split_message[0]
        parsed_message = {"type": message_type, "data": {}}

        if message_type in ("ACC", "GYR"):
            parsed_message["data"] = {
                "x": split_message[1],
                "y": split_message[2],
                "z": split_message[3],
            }
        elif "LID" in split_message:
            parsed_message["data"] = {
                "left": split_message[1],
                "middle": split_message[2],
                "right": split_message[3],
            }
        elif message_type in ("COM", "BAT"):
            parsed_message["data"] = {
                "x": split_message[1],
            }
        elif message_type in ("RPM", "TMP", "WET", "GPS"):
            parsed_message["data"] = {"x": split_message[1], "y": split_message[2]}
        elif message_type in ("GPS"):
            parsed_message["data"] = {"long": split_message[1], "lat": split_message[2]}

        return str(json.dumps(parsed_message, indent=4))

    return {}
