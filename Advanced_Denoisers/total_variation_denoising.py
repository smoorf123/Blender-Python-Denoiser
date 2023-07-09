import sys
sys.path.insert(0, "C:/Users/Somil/Desktop/VSCode-Python/Blender-Denoiser/Required_Dependencies/cv2")
sys.path.insert(0, "C:/Users/Somil/Desktop/VSCode-Python/Blender-Denoiser/Required_Dependencies/skimage")

from cv2 import imread
from skimage.restoration import denoise_tv_bregman


# Apply total variation denoising
# weight specifies the degree of denoising, channel_axis specifies the axis of
# color channels with -1 being the last axis (color)
def tv_dn(image):
    img = imread(image)
    filtered_image = denoise_tv_bregman(img, weight=10, channel_axis=-1)
    return filtered_image
