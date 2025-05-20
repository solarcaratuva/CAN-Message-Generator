import json
import cantools as ct
import random as rand
import math
import os
import sys
from tqdm import trange

TIMESTAMP_RATE = 1.1

dbc_files = os.listdir("./CAN-messages")
dbs = [ct.db.load_file(f"./CAN-messages/{file}") for file in dbc_files if file.endswith(".dbc")]

file_map = dict()
message_map = dict()


def setup_maps() -> None:
    for template in config:
        handled = False
        for db in dbs:
            for message in db.messages:
                if message.name == template:
                    message_map[template] = message
                    file_map[template] = db
                    handled = True
                    break
        if not handled:
            print(f"ERROR: Message type \"{template}\" not found in any DBC file.")
            exit(1)


def generate_message(message_type: str, data: dict, time: int) -> str:
    db = file_map[message_type]
    message = message_map[message_type]

    default_data = {signal.name: 0 for signal in message.signals}
    data = default_data | data

    try:
        encoded_message_bytes = db.encode_message(message_type, data)
    except Exception as e:
        print(f"Error encoding message: {e}")
        exit(1)
    encoded_message_hex = encoded_message_bytes.hex()
    encoded_message_hex = (message.length * 2 - len(encoded_message_hex)) * "0" + encoded_message_hex

    id_hex = hex(message.frame_id)[2:]
    sec = str(time % 60).zfill(2)
    min = str(time // 60 % 60).zfill(2)
    hour = str(time // 3600).zfill(2)

    text = f"{hour}:{min}:{sec} DEBUG /root/Rivanna2/Common/src/MainCANInterface.cpp:40: Sent CAN message with ID 0x{id_hex} Length {message.length} Data 0x{encoded_message_hex}"
    return text


def main() -> None:
    if len(sys.argv) != 3:
        print("ERROR: Expected 2 command line arguments: config json file path, number of messages to generate")
        exit(1)
    config_path = sys.argv[1]
    if not os.path.exists(config_path):
        print(f"ERROR: File \"{config_path}\" not found.")
        exit(1)
    with open(config_path, "r") as file:
        global config
        config = json.load(file)
    num_messages = int(float(sys.argv[2]))

    setup_maps()
    templates_keys = list(config.keys())
    
    with open("out.txt", "w") as file:
        time = 0
        for i in trange(num_messages, leave=False, desc="Generating messages", unit="message"):
            messageType = rand.choice(templates_keys)
            template = config[messageType]
            try:
                messageData = {key: eval(str(template[key]), None, {"i": i}) for key in template.keys()}
            except Exception as e:
                print(f"Error when evaluating a statement in {config_path} for {messageType}: \n{e}")
                exit(1)
            text = generate_message(messageType, messageData, time)
            file.write(text+"\n")
            time += int(rand.random() * TIMESTAMP_RATE)

    print("Done!")


if __name__ == '__main__':
    main()