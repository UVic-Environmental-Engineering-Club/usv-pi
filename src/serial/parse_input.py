import json

ACC_GYR_Value = {'x': -1, 'y': -1, 'z': -1}
LID_Value = {'left': -1, 'middle': -1, 'right': -1}
COM_BAT_Value = {'x': -1}
RPM_TMP_WET_GPS_Value = {'x': -1, 'y': -1}

Arrays = [['x', 'y', 'z'], ['left', 'middle', 'right']]

def dataUpdater(value, myJson, splitMessage, array, size):
    myData = value
    i = 1
    while i < size:
        value = splitMessage[i]
        myData[array[i - 1]] = value
        i = i + 1
    myJson["data"] = myData


def parse_string(message: str) -> str:
    if message is not None:
        splitMessage = message.split("-")
        myType = splitMessage[0]
        myJson = {"type": myType, "data": None}

        if myType in ("ACC", "GYR"):
            dataUpdater(ACC_GYR_Value, myJson, splitMessage, Arrays[0], len(splitMessage))
        elif "LID" in splitMessage:
            dataUpdater(LID_Value, myJson, splitMessage, Arrays[1], len(splitMessage))
        elif myType in ("COM", "BAT"):
            dataUpdater(COM_BAT_Value, myJson, splitMessage, Arrays[0], 2)
        elif myType in ("RPM", "TMP", "WET", "GPS"):
            dataUpdater(RPM_TMP_WET_GPS_Value, myJson, splitMessage, Arrays[0], 3)
        return str(json.dumps(myJson, indent=4))
    return ""