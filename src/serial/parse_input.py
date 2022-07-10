from typing import Dict

from src.constants import SENSOR_NAMES


def parse_string(message: str) -> Dict[str, float]:
    if message is not None:
        split_message = message.split(":")
        message_type = split_message[0]
        parsed_message = {"type": message_type, "data": {}}

        if message_type not in SENSOR_NAMES:
            return {}

        if message_type in ("ACC", "GYR", "MAG"):
            parsed_message["data"] = {
                "x": split_message[1],
                "y": split_message[2],
                "z": split_message[3],
            }
        elif message_type in ("LID"):
            parsed_message["data"] = {
                "left": split_message[1],
                "middle": split_message[2],
                "right": split_message[3],
            }
        elif message_type in ("BAT"):
            parsed_message["data"] = {
                "volatage": split_message[1],
            }
        elif message_type in ("RPM", "TMP", "WET"):
            parsed_message["data"] = {
                "left": split_message[1],
                "right": split_message[2],
            }
        elif message_type in ("GPS"):
            parsed_message["data"] = {"long": split_message[1], "lat": split_message[2]}
        elif message_type in ("GPSSTAT"):
            parsed_message["data"] = {"sats": split_message[1], "fix": split_message[2]}

        return parsed_message

    return {}
