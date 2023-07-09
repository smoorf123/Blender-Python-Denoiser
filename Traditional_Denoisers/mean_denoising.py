import sys
sys.path.insert(0, "C:/Users/Somil/Desktop/VSCode-Python/Blender-Denoiser/Required_Dependencies/cv2")

from cv2 import imread, blur

# Apply mean filtering with a 5x5 kernel
def mean_dn(image):
    img = imread(image)
    filtered_image = blur(img, (5, 5))
    return filtered_image
