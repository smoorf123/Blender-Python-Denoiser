import sys
sys.path.insert(0, "C:/Users/Somil/Desktop/VSCode-Python/Blender-Denoiser/Required_Dependencies/cv2")

from cv2 import imread, GaussianBlur

# Apply gaussian filtering with a 5x5 kernel, 0 implying that the
# standard deviation is calculated automatically
def gaussian_dn(image):
    img = imread(image)
    filtered_image = GaussianBlur(img, (5, 5), 0)
    return filtered_image

