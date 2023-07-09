import cv2  # Import the OpenCV library

# Apply bilateral filtering
# 9 is the diameter of the pixel neighborhood used,75 is the sigma
# value for color space, 75 is the sigma value for coordinate space
def bilateral_dn(image):
    img = cv2.imread(image)
    filtered_image = cv2.bilateralFilter(img, 9, 75, 75)
    return filtered_image
