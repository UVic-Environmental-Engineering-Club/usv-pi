import asyncio
from enum import Enum, auto
from typing import Tuple, Union

from src.constants import DATA, LID_COLLECTION, State
from src.driver import driver


class ShoreDirection(Enum):
    LEFT = auto()
    RIGHT = auto()


class CDState(Enum):
    TURN_LEFT = auto()
    TURN_RIGHT = auto()
    CLEAR_OBSTACLE_LEFT = auto()
    CLEAR_OBSTACLE_RIGHT = auto()


def get_lid_data() -> Tuple[int, int, int]:
    lid_doc = LID_COLLECTION.find_one(sort=[("timestamp", -1)])
    lid_data = lid_doc["data"]

    left = int(lid_data["left"]) / 10
    middle = int(lid_data["middle"]) / 10
    right = int(lid_data["right"]) / 10

    return (left, middle, right)


async def collision_detection_loop():
    """Lidar data is formatted is XYZ,
    where X is 10s, Y is ones, and Z is a decimal
    Units: meters
    """
    cd_state: Union[None, CDState] = None
    prev_state: Union[None, State] = None

    while True:
        await asyncio.sleep(1)

        left, middle, right = get_lid_data()

        if middle > 20 and cd_state is None:
            continue

        if DATA["state"] != State.COLLISION_DETECTION:
            prev_state = DATA["state"]

        DATA["state"] = State.COLLISION_DETECTION

        if cd_state is None:
            cd_state = (
                CDState.TURN_LEFT
                if locate_shore() == ShoreDirection.RIGHT
                else CDState.TURN_RIGHT
            )

        print("after", cd_state)

        if cd_state is CDState.TURN_LEFT:
            while middle < 20 or right < 20:
                # driver.turn_left()
                await asyncio.sleep(1)
                left, middle, right = get_lid_data()

            cd_state = CDState.CLEAR_OBSTACLE_LEFT

        if cd_state is CDState.TURN_RIGHT:
            while middle < 20 or left < 20:
                # driver.turn_right()
                await asyncio.sleep(1)
                left, middle, right = get_lid_data()

            cd_state = CDState.CLEAR_OBSTACLE_RIGHT

        if cd_state in (
            CDState.CLEAR_OBSTACLE_LEFT,
            CDState.CLEAR_OBSTACLE_RIGHT,
        ):
            if (cd_state == CDState.CLEAR_OBSTACLE_LEFT and left < 20) or (
                cd_state == CDState.CLEAR_OBSTACLE_RIGHT and right < 20
            ):
                driver.forward()
            else:
                cd_state = None
                DATA["state"] = prev_state
                prev_state = None


def locate_shore() -> ShoreDirection:
    left, middle, right = get_lid_data()

    if left > right:
        return ShoreDirection.LEFT
    else:
        return ShoreDirection.RIGHT
