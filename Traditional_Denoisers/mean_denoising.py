import cv2  # Import the OpenCV library

# Apply mean filtering with a 5x5 kernel
def mean_dn(image):
    img = cv2.imread(image)
    filtered_image = cv2.blur(img, (5, 5))
    return filtered_image
