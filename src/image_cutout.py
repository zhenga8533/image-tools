from dotenv import load_dotenv
from util.logger import Logger
import cv2
import logging
import numpy as np
import os


def zoom_image(image: np.ndarray, logger: Logger) -> np.ndarray:
    """
    Zoom and pan an image.

    :param: image - Image to zoom and pan
    :param: logger - Logger object
    :return: Zoomed and panned image
    """

    [width, height, _] = image.shape
    cv2.resizeWindow("Image", width, height)
    zoomed_image = image

    zoom = 1
    origin = [width // 2, height // 2]

    # Display instructions
    logger.log(logging.INFO, "Zoom and pan the image using the following controls:")
    logger.log(logging.INFO, "  '+' - Zoom in")
    logger.log(logging.INFO, "  '-' - Zoom out")
    logger.log(logging.INFO, "  'w' - Pan up")
    logger.log(logging.INFO, "  'a' - Pan left")
    logger.log(logging.INFO, "  's' - Pan down")
    logger.log(logging.INFO, "  'd' - Pan right")
    logger.log(logging.INFO, "  'r' - Reset zoom and pan")
    logger.log(logging.INFO, "  'Enter' - Submit")
    logger.log(logging.INFO, "  'Esc' - Exit program")

    while True:
        # Display the zoomed/panned image
        x1 = max(0, int(origin[0] - width / (2 * zoom)))
        x2 = min(width, int(origin[0] + width / (2 * zoom)))
        y1 = max(0, int(origin[1] - height / (2 * zoom)))
        y2 = min(height, int(origin[1] + height / (2 * zoom)))
        zoomed_image = image[
            y1:y2,
            x1:x2,
        ]
        cv2.imshow(
            "Image",
            zoomed_image,
        )

        # Wait for key press
        key = cv2.waitKey(1) & 0xFF
        if key == 255:
            continue
        logger.log(logging.DEBUG, f"Key pressed: {chr(key)}")

        # Handle zoom in/out with '+' and '-'
        if key == ord("="):
            zoom += 0.1
            logger.log(logging.DEBUG, f"Zoomed in to {zoom}")
        elif key == ord("-"):
            zoom -= 0.1
            logger.log(logging.DEBUG, f"Zoomed out to {zoom}")

        # Handle panning with 'w', 'a', 's', 'd'
        elif key == ord("w"):
            origin[1] -= 10
            logger.log(logging.DEBUG, f"Panned up to {origin}")
        elif key == ord("a"):
            origin[0] -= 10
            logger.log(logging.DEBUG, f"Panned left to {origin}")
        elif key == ord("s"):
            origin[1] += 10
            logger.log(logging.DEBUG, f"Panned down to {origin}")
        elif key == ord("d"):
            origin[0] += 10
            logger.log(logging.DEBUG, f"Panned right to {origin}")
        elif key == ord("r"):
            zoom = 1
            origin = [width // 2, height // 2]
            logger.log(logging.DEBUG, f"Reset zoom and pan to {zoom} and {origin}")

        # Handle submit with 'Enter'
        elif key == ord("\r"):
            logger.log(logging.INFO, "Submitted zoom and pan")
            break
        elif key == ord("\x1b"):
            logger.log(logging.INFO, "Exiting program")
            exit(0)

    return zoomed_image


def main():
    # Load environment variables
    load_dotenv()
    LOG = os.getenv("LOG") == "True"

    # Initialize logger
    logger = Logger("main", "logs/main.log", LOG)

    # Read input image
    image_path = input("Enter the path of the image: ")
    image = cv2.imread(image_path)

    # Zoom and pan the image, then select a region to cut out
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    image = zoom_image(image, logger)
    cutout_box = cv2.selectROI("Image", image)
    cv2.destroyAllWindows()

    # Crop the image
    logger.log(logging.INFO, f"Cutting out region {cutout_box}")
    x1 = cutout_box[0]
    y1 = cutout_box[1]
    x2 = cutout_box[0] + cutout_box[2]
    y2 = cutout_box[1] + cutout_box[3]
    cutout = image[y1:y2, x1:x2]

    # Save new cutout image
    file_name = image_path.split("/")[-1].split(".")[0]
    save_path = image_path.replace(file_name, f"{file_name}_cutout")
    copy_num = 1
    while os.path.exists(save_path):
        save_path = image_path.replace(file_name, f"{file_name}_cutout_{copy_num}")
        copy_num += 1
    logger.log(logging.INFO, f"Saving cutout image to {save_path}")
    cv2.imwrite(save_path, cutout)


if __name__ == "__main__":
    main()
