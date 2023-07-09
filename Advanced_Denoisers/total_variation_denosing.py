# Import the necessary dependencies from the scikit-image library
from skimage.restoration import denoise_tv_bregman
import cv2  # Import the OpenCV library

# Apply total variation denoising
# weight specifies the degree of denoising, channel_axis specifies the axis of
# color channels with -1 being the last axis (color)
def tv_dn(image):
    img = cv2.imread(image)
    filtered_image = denoise_tv_bregman(img, weight=10, channel_axis=-1)
    return filtered_image
