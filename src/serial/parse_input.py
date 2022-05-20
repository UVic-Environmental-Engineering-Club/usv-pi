def template_creator(message_type):
    base_message = ""
    if message_type == "type2":
        # put two data subfield
    elif message_type = "type3":
        # put three data subfield
    else:    
        # put 4 data subfield
def parse_string(message: str) -> str:

    split_message = message.split("-")

    #type = str(split_message.pop(0))

    splitted_message_length = len(split_message)

    message_type= {"type2": 2, "type3":3, "type4": 4}
    message_template = template_creator(message_type)
    json_message = '{"type": "ACC", "data": {"x": 121, "y": 232, "z": 1212}}'
    

    return {"type": type, "data": split_message}
