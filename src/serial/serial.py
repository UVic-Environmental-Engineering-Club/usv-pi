""" Functions for things related to serial and pySerial """
from os import system
import time
from serial import Serial
from typing import List, Tuple, Any
from src.events.event_type import EventType
import json

def serial_loop(event_list: List[Tuple[EventType, Any]], serial : Serial):
    """Serial loop with two threads, one for reading, one for writing"""
    """https://stackoverflow.com/questions/39127158/small-example-for-pyserial-using-threading"""

    #read serial info and open
    with open(file="config.json", mode="r", encoding="utf-8") as file:
        config = json.load(file)
        serial = Serial(config["port"], config["baudrate"], timeout = config["timeout"])
        file.close()

    while True:
        print("serial process!")
        try : 
            if(serial.is_open == True) : print(serial.read())
        except: 
            print ("Error reading from serial")
            break
        time.sleep(3) 

