import warnings
from typing import Union
import serial
import time

from backend.utils import take_snapshot
from loguru import logger

ARDUINO_STATUS_KEY = {-1: "disabled", 0: "ready", 1: "armed", 2: "moving"}
ARDUINO_INSTRUCTION_KEY = {"trigger_move": 1, "cancel_move": -9, "request_status": 5}

ARDUINO_STATUS = ARDUINO_STATUS_KEY[-1]

def search_and_connect_arduino():
    arduino_ports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if 'Arduino' in p.description
    ]
    if not arduino_ports:
        raise IOError("No Arduino found")
    if len(arduino_ports) > 1:
        warnings.warn('Multiple Arduinos found - using the first')

    return serial.Serial(port=arduino_ports[0], baudrate=115200, timeout=0.1)

ser = search_and_connect_arduino()

def parse_message(binary_string):
    return int(binary_string.decode('ascii').strip().split("\n")[0])

def sync_arduino_state(): 
    global ARDUINO_STATUS
    while True: 
        line = ser.readline()
        if line:
            ARDUINO_STATUS = ARDUINO_STATUS_KEY[parse_message(line)]
            logger.info(f"Updated Arduino state to: {ARDUINO_STATUS}")
        time.sleep(0.5)

def write_instruction_arduino(instruction: int) -> Union[None, int]:
    global ARDUINO_STATUS

    if instruction == ARDUINO_INSTRUCTION_KEY["request_status"]:
        ser.write(bytes(instruction, 'utf-8'))
        time.sleep(0.05)
        ARDUINO_STATUS = parse_message(ser.readline())
        return ARDUINO_STATUS
    
    ser.write(bytes(instruction, 'utf-8'))

    logger.info(f"Wrote instruction {instruction} to Arduino")



def write_read(num): 
    ser.write(bytes(num, 'utf-8'))
    time.sleep(0.05)
    return parse_message(ser.readline())

if __name__ == "__main__":
    while True:
        num = input("Enter command: ")
        if num == str(1):
            take_snapshot()

        val = write_read(num)
        print(str(val))  # printing the value
