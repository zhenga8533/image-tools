import cv2


def zoom_image(image):
    [width, height, _] = image.shape
    cv2.resizeWindow("Image", width, height)
    zoomed_image = image

    zoom = 1
    origin = [width // 2, height // 2]

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
        key = cv2.waitKey(1)
        if key == 255:
            continue

        # Handle zoom in/out with '+' and '-'
        elif key == ord("="):
            zoom += 0.1
        elif key == ord("-"):
            zoom -= 0.1

        # Handle panning with 'w', 'a', 's', 'd'
        elif key == ord("w"):
            origin[1] -= 10
        elif key == ord("a"):
            origin[0] -= 10
        elif key == ord("s"):
            origin[1] += 10
        elif key == ord("d"):
            origin[0] += 10
        elif key == ord("r"):
            zoom = 1
            origin = [width // 2, height // 2]

        # Handle submit with 'Enter'
        elif key == ord("\r"):
            break

    return zoomed_image


def main():
    # Read input image
    image_path = input("Enter the path of the image: ")
    image = cv2.imread(image_path)

    # Open the image in a window
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    image = zoom_image(image)
    cutout_box = cv2.selectROI("Image", image)
    cv2.destroyAllWindows()

    # Crop the image
    x1 = cutout_box[0]
    y1 = cutout_box[1]
    x2 = cutout_box[0] + cutout_box[2]
    y2 = cutout_box[1] + cutout_box[3]
    cutout = image[y1:y2, x1:x2]

    # Save new cutout image
    file_name = image_path.split("/")[-1].split(".")[0]
    save_path = image_path.replace(file_name, f"{file_name}_cutout_{x1}_{y1}_{x2}_{y2}")
    cv2.imwrite(save_path, cutout)


if __name__ == "__main__":
    main()
