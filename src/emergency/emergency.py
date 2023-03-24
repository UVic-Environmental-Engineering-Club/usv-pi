from src.constants import WET_COLLECTION, TMP_COLLECTION, BAT_COLLECTION


def get_wet_data() -> tuple:
    """data is formatted is XY,
    where X is left, and Y is right
    Units: % humidity?
    """
    wet_doc = WET_COLLECTION.find_one(sort=[("timestamp", -1)])
    wet_data = wet_doc["data"]

    left = int(wet_data["left"])
    right = int(wet_data["right"])

    return (left, right)


def get_tmp_data() -> tuple:
    """data is formatted is XY,
    where X is left, and Y is right
    Units: degree celsius
    """
    tmp_doc = TMP_COLLECTION.find_one(sort=[("timestamp", -1)])
    tmp_data = tmp_doc["data"]

    left = int(tmp_data["left"])
    right = int(tmp_data["right"])

    return (left, right)


def get_bat_data() -> int:
    bat_doc = BAT_COLLECTION.find_one(sort=[("timestep", -1)])
    bat_data = bat_doc["data"]

    return int(bat_data)


async def emergency_interrupt() -> bool:
    # first, find threshold of each data
    # then if curr data > threshold trigger interrupt
    return False
