from dotenv import load_dotenv
from util.logger import Logger
import cv2
import logging
import numpy as np
import os


def resize_image(image: np.ndarray, width: int, height: int, logger: Logger) -> np.ndarray:
    """
    Resize an image to the target width and height by cropping and padding.

    :param image: Image to resize
    :param width: Target width
    :param height: Target height
    :param logger: Logger object
    :return: Resized image
    """

    # Get current image dimensions
    image_height, image_width = image.shape[:2]

    # Crop horizontally if width is smaller than the current width
    if image_width > width:
        offset_x = (image_width - width) // 2
        image = image[:, offset_x : offset_x + width]

    # Crop vertically if height is smaller than the current height
    if image_height > height:
        image_height, image_width = image.shape[:2]
        offset_y = (image_height - height) // 2
        image = image[offset_y : offset_y + height, :]

    # Padding if the image is smaller than the target size
    image_height, image_width = image.shape[:2]

    pad_x = max(0, width - image_width)
    pad_y = max(0, height - image_height)

    # Calculate padding for each side to keep it centered
    pad_x_left = pad_x // 2
    pad_x_right = pad_x - pad_x_left
    pad_y_top = pad_y // 2
    pad_y_bottom = pad_y - pad_y_top

    # Add border (padding) to reach the target size
    resized_image = cv2.copyMakeBorder(
        image, pad_y_top, pad_y_bottom, pad_x_left, pad_x_right, cv2.BORDER_CONSTANT, value=[0, 0, 0, 0]
    )

    # Log the final size
    logger.log(logging.INFO, f"Image resized (center-cropped/padded) to {width}x{height}")
    return resized_image


def main():
    load_dotenv()
    LOG = os.getenv("LOG") == "True"
    IMAGE_PATH = os.getenv("IMAGE_PATH")
    IMAGE_DIRECTORY = os.getenv("IMAGE_DIRECTORY")
    RESIZE_WIDTH = int(os.getenv("RESIZE_WIDTH"))
    RESIZE_HEIGHT = int(os.getenv("RESIZE_HEIGHT"))

    logger = Logger("main", "logs/image_resize.log", LOG)

    def save_image(image: np.ndarray, image_path: str, logger: Logger) -> None:
        """
        Save an image to a file.

        :param image: Image to save
        :param image_path: Current image path
        :param logger: Logger object
        """

        file_name = image_path.split("/")[-1].split(".")[0]
        if file_name.find("_resized") != -1:
            logger.log(logging.INFO, "Skipping already resized image")
            return
        save_path = image_path.replace(file_name, f"{file_name}_{RESIZE_WIDTH}x{RESIZE_HEIGHT}_resized")
        logger.log(logging.INFO, f"Saving resized image to {save_path}")
        cv2.imwrite(save_path, image)
        logger.log(logging.INFO, "Resized image saved")

    # Check if IMAGE_DIRECTORY is valid
    if not os.path.isdir(IMAGE_DIRECTORY):
        logger.log(logging.INFO, "Image directory not found, attempting to use IMAGE_PATH")
        image = cv2.imread(IMAGE_PATH, cv2.IMREAD_UNCHANGED)
        if image is None:
            logger.log(logging.ERROR, "Invalid image path")
            exit(1)
        logger.log(logging.INFO, f"Image loaded from {IMAGE_PATH}")

        # Resize image (center image and add/remove pixels)
        resized_image = resize_image(image, RESIZE_WIDTH, RESIZE_HEIGHT, logger)
        save_image(resized_image, IMAGE_PATH, logger)
    else:
        logger.log(logging.INFO, f"Image directory found at {IMAGE_DIRECTORY}")

        # Resize all images in the directory
        for image_name in os.listdir(IMAGE_DIRECTORY):
            image_path = os.path.join(IMAGE_DIRECTORY, image_name)
            image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            if image is None:
                logger.log(logging.ERROR, f"Invalid image path: {image_path}")
                continue
            logger.log(logging.INFO, f"Image loaded from {image_path}")

            # Resize image (center image and add/remove pixels)
            resized_image = resize_image(image, RESIZE_WIDTH, RESIZE_HEIGHT, logger)
            save_image(resized_image, image_path, logger)


if __name__ == "__main__":
    main()
