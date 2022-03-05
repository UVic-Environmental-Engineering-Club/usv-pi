from src.driver.driver import add_gps_coord

def parse_string(str):

    split = str.split('-')
    split.pop(0)
    print(split)
    
    if("ACC" in str):     
        "logic for acc"    
    
    elif("GYR" in str):
        "logic for GYR"

    elif("COM" in str):
        "logic for COM"
    
    elif("LID" in str):
        "logic for LID"

    elif("RPM" in str):
        "logic for RPM"
    
    elif("TMP" in str):
        "logic for TMP"

    elif("WET" in str):
        "logic for WET"
    
    elif("GPS" in str):
        "logic for GPS"
