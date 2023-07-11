import cv2

# Apply median filtering with a 5x5 kernel
def median_dn(image):
    img = cv2.imread(image)
    filtered_image = cv2.medianBlur(img, 5)
    return filtered_image