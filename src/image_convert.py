from dotenv import load_dotenv
from util.logger import Logger
import cv2
import logging
import os

if __name__ == "__main__":
    load_dotenv()
    LOG = os.getenv("LOG") == "True"

    # Initialize logger
    logger = Logger("main", "logs/main.log", LOG)

    # Get image path and type to convert to
    image_path = input("Enter the path of the image: ")
    convert_type = input("Enter type of file to convert to: ")

    # Load image
    image = cv2.imread(image_path)
    if image is None:
        logger.log(logging.ERROR, "Invalid image path")
        exit(1)
    logger.log(logging.INFO, f"Image loaded from {image_path}")

    # Convert image
    logger.log(logging.INFO, f"Converting image to {convert_type}")
    base_name = ".".join(image_path.split("\\")[-1].split(".")[:-1])
    cv2.imwrite(f"{base_name}.{convert_type}", image)
    logger.log(logging.INFO, f"Image converted to {convert_type}")
