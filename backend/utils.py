import cv2

import datetime

from PIL import Image

camera = cv2.VideoCapture(0)

from loguru import logger 


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
    filename = "_".join([basename, suffix])  # e.g. 'snapshot_120508_171442'

    image.save(f"{filename}.png", "png")

    logger.info(f"Saved snapshot under {filename}")
    return f"{filename}.png"