import cv2  # Import the OpenCV library

# Apply gaussian filtering with a 5x5 kernel, 0 implying that the
# standard deviation is calculated automatically
def gaussian_dn(image):
    img = cv2.imread(image)
    filtered_image = cv2.GaussianBlur(img, (5, 5), 0)
    return filtered_image

