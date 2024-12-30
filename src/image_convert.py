from dotenv import load_dotenv
from util.logger import Logger
import cv2
import logging
import os

if __name__ == "__main__":
    load_dotenv()
    LOG = os.getenv("LOG") == "True"
    IMAGE_PATH = os.getenv("IMAGE_PATH")
    CONVERT_TYPE = os.getenv("CONVERT_TYPE")

    # Initialize logger
    logger = Logger("main", "logs/image_convert.log", LOG)

    # Load image
    image = cv2.imread(IMAGE_PATH)
    if image is None:
        logger.log(logging.ERROR, "Invalid image path")
        exit(1)
    logger.log(logging.INFO, f"Image loaded from {IMAGE_PATH}")

    # Convert image
    logger.log(logging.INFO, f"Converting image to {CONVERT_TYPE}")
    base_name = ".".join(IMAGE_PATH.split("\\")[-1].split(".")[:-1])
    cv2.imwrite(f"{base_name}.{CONVERT_TYPE}", image)
    logger.log(logging.INFO, f"Image converted to {CONVERT_TYPE}")
