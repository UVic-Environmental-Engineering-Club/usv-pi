""" Main loop that is run on the Raspberry Pi on the USV 🛳⚓️ """
from typing import List, Optional, Dict, Callable, Any, Tuple
from multiprocessing import Process, Manager
from serial import Serial
from src.serial.serial import serial_loop
from src.driver.driver import driver_loop
from src.events.events import run_event_loop
from src.events.event_type import EventType
from src.database.database_listener import setup_database_handlers
from src.serial.serial_listener import setup_serial_handlers
from src.socketio.socketio_listener import setup_socketio_handlers
from src.data_classes.sensor.data_in import GpsCoord
import json


route: List[GpsCoord] = []
serial: Optional[Serial] = None
paused_gps_coord: Optional[GpsCoord] = None
processes: Dict[str, Process] = {}


def run():
    """Used to start the loop in __main__"""
    with Manager() as manager:
        subscribers: Dict[EventType, List[Callable[[Any], Any]]] = manager.dict()
        event_list: List[Tuple[EventType, Any]] = manager.list()
        setup_database_handlers(manager, subscribers)
        setup_serial_handlers(manager, subscribers)
        setup_socketio_handlers(manager, subscribers)
        processes["driver"] = Process(target=driver_loop, args=(event_list,))
        processes["serial"] = Process(target=serial_loop,  args=(event_list, serial))
        processes["event_loop"] = Process(target=run_event_loop, args=(subscribers, event_list))

        for _, process in processes.items():
            process.start()

        for _, process in processes.items():
            process.join()
