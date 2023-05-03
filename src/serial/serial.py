""" Functions for things related to serial and pySerial """
"""We are using thread6 to import threading"""
import asyncio
import threading
from src.events.event_type import EventType
from src.events.events import post_event
from src.constants import SERIAL

thread_flag = None


def reading():
    global thread_flag
    thread_flag = 'reading'
    while thread_flag != 'reading': asyncio.sleep( 0.001 )

    while thread_flag == 'reading':
        """Do reading"""
        if SERIAL.is_open == True:
            message = SERIAL.readline().decode("utf8").strip()
            if message:
                post_event(EventType.SERIAL_IN, message)


    thread_flag = "reading done"


"""Figure out what do we write"""
def writing():
    global thread_flag
    thread_flag = 'writing'
    while thread_flag != 'writing': asyncio.sleep( 0.001 )

    while thread_flag == 'writing':
        """Do writing"""
        if SERIAL.is_open == True:
            message = """What is the message?"""
            if message:
                post_event(EventType.SERIAL_OUT, message)
    

    thread_flag = "writing done"




async def serial_loop():
    """Serial loop with two threads, one for reading, one for writing"""
    """https://stackoverflow.com/questions/39127158/small-example-for-pyserial-using-threading"""
    await asyncio.sleep(1) 

    while True:
        await asyncio.sleep(0.001)
        if not SERIAL:
            print("Serial not initialized")
            continue

        try:
            t1 = threading.Thread(target = reading)
            t2 = threading.Thread(target = writing, args=[])
            """Figure out what is args for this case"""
            t1.start()
            asyncio.sleep(0.5)
            """This could be the reading/writing speed"""
            t2.start()
            asyncio.sleep(0.5)
            """This could be the reading/writing speed"""


        except Exception as e:
            print("Error reading from serial", e)
            break
