import asyncio
import json

from pymongo import MongoClient
import socketio
from typing import Optional
from serial import Serial
from typing import List, Optional, Dict, Callable, Any, Tuple
from src.data_classes.sensor.data_in import GpsCoord
from src.events.event_type import EventType


SERIAL: Optional[Serial] = None
MONGO_CLIENT: Optional[MongoClient] = None

with open(file="config.json", mode="r", encoding="utf-8") as file:
    config = json.load(file)
    try:
        SERIAL = Serial(config["port"], config["baudrate"], timeout=config["timeout"])
    except Exception as error:
        print("Could not open serial port.", error)
        SERIAL = None

    try:
        MONGO_CLIENT = MongoClient(config["mongo_url"])
    except Exception as error:
        print("Could not open database.", error)
        MONGO_CLIENT = None

ROUTE: List[GpsCoord] = []
SHORE: List[GpsCoord] = []
SUBSCRIBERS: Dict[EventType, List[Callable[[Any], Any]]] = {}
EVENT_LIST: asyncio.Queue[Tuple[EventType, Any]] = asyncio.Queue()

SIO = socketio.AsyncClient()

USV_DB = MONGO_CLIENT.usv
SENSOR_DATA_COLLECTION = USV_DB.sensor_data
