import sys
sys.path.insert(0, "C:/Users/Somil/Desktop/VSCode-Python/Blender-Denoiser/Required_Dependencies/cv2")

from cv2 import imread, bilateralFilter

# Apply bilateral filtering
# 9 is the diameter of the pixel neighborhood used,75 is the sigma
# value for color space, 75 is the sigma value for coordinate space
def bilateral_dn(image):
    img = imread(image)
    filtered_image = bilateralFilter(img, 9, 75, 75)
    return filtered_image
