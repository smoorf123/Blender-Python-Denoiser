import sys
sys.path.insert(0, "C:/Users/Somil/Desktop/VSCode-Python/Blender-Denoiser/Required_Dependencies/cv2")

from cv2 import imread, medianBlur

# Apply median filtering with a 5x5 kernel
def median_dn(image):
    img = imread(image)
    filtered_image = medianBlur(img, 5)
    return filtered_image