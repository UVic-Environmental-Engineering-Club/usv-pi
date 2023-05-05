import asyncio
import threading
import time
from src.events.event_type import EventType
from src.events.events import post_event
from src.constants import SERIALccb #, SERIALpdb
""" Functions for things related to serial and pySerial """
""" We are using thread6 to import threading """


thread_flag = None


def readingccb():
    global thread_flag
    thread_flag = 'reading'
    while thread_flag != 'reading': time.sleep( 0.001 )

    """Do reading"""
    while thread_flag == 'reading':
        if SERIALccb.is_open is True:
            message = SERIALccb.readline().decode("utf8").strip()
            if message:
                post_event(EventType.SERIAL_IN, message)


    thread_flag = "reading done"


def readingpdb():
    global thread_flag
    thread_flag = 'reading'
    while thread_flag != 'reading': time.sleep( 0.001 )
    
    """Do reading"""
    while thread_flag == 'reading':
        if SERIALpdb.is_open is True:
            message = SERIALpdb.readline().decode("utf8").strip()
            if message:
                post_event(EventType.SERIAL_IN, message)


    thread_flag = "reading done"


"""Figure out what do we write"""
def writingccb():
    global thread_flag
    thread_flag = 'writing'
    while thread_flag != 'writing': time.sleep( 0.001 )

    while thread_flag == 'writing':
        """Do writing"""
        if SERIALccb.is_open is True:
            message = """What is the message?"""
            if message:
                post_event(EventType.SERIAL_OUT, message)
    

    thread_flag = "writing done"

"""Figure out what do we write"""
def writingpdb():
    global thread_flag
    thread_flag = 'writing'
    while thread_flag != 'writing': time.sleep( 0.001 )

    while thread_flag == 'writing':
        """Do writing"""
        if SERIALpdb.is_open is True:
            message = """What is the message?"""
            if message:
                post_event(EventType.SERIAL_OUT, message)
    

    thread_flag = "writing done"

def stop():
    global thread_flag
    thread_flag = 'stop'


async def serial_loop():
    """Serial loop with two threads, one for reading, one for writing"""
    """https://stackoverflow.com/questions/39127158/small-example-for-pyserial-using-threading"""
    await asyncio.sleep(1) 

    while True:
        await asyncio.sleep(0.001)
        if not SERIALccb or not SERIALpdb:
            print("Serial not initialized")
            continue

        try:
            t1 = threading.Thread(target = readingccb)
            t2 = threading.Thread(target = writingccb, args=[])
            """t3 = threading.Thread(target = readingpdb)
            t4 = threading.Thread(target = writingpdb, args=[])"""
            """Figure out what is args for this case"""
            t1.start()
            asyncio.sleep(0.25)
            """This could be the reading/writing speed"""
            t2.start()
            asyncio.sleep(0.25)
            """This could be the reading/writing speed"""
            """t3.start()
            asyncio.sleep(0.25)"""
            """This could be the reading/writing speed"""
            """t4.start()
            asyncio.sleep(0.25)"""
            """This could be the reading/writing speed"""


        except Exception as e:
            print("Error reading from serial", e)
            break
