# Import the necessary dependencies from the scikit-image library
from skimage.restoration import denoise_tv_bregman
import cv2  # Import the OpenCV library

# Read the image from appropriate path
image = cv2.imread('./Blender-Denoiser/noisy-img.png')

# Display the image
cv2.imshow("Image", image)

# Apply total variation denoising
# weight specifies the degree of denoising, channel_axis specifies the axis of
# color channels with -1 being the last axis (color)
def tv_dn(image):
    filtered_image = denoise_tv_bregman(image, weight=10, channel_axis=-1)
    return filtered_image


# Display the filtered image
cv2.imshow('Filtered Image', tv_dn(image))
cv2.waitKey(0)  # Wait for a key press to exit
cv2.destroyAllWindows()  # Close all windows
