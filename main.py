import serial 
import time 
import cv2

import datetime

from PIL import Image



camera = cv2.VideoCapture(0)

# Takes a single picture from the current video capture device.
def get_image() -> Image.Image:
  retval, image = camera.read()
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  image = Image.fromarray(image)
  return image

def take_snapshot(): 
    image = get_image() 

    basename = "snapshot"
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    filename = "_".join([basename, suffix]) # e.g. 'snapshot_120508_171442' 

    image.save(f"{filename}.png", 'png')
    

arduino = serial.Serial(port='/dev/cu.usbmodem11301', baudrate=115200, timeout=.1)

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

while True:
    num = input("Enter command: ")
    val = write_read(num)
    print(str(val)) # printing the value

    #take_snapshot()