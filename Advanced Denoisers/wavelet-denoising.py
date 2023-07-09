# Import the necessary dependencies from the scikit-image library
from skimage.restoration import denoise_wavelet, cycle_spin
from skimage import io, img_as_float

import numpy as np  # Import the NumPy library
import cv2  # Import the OpenCV library

# Read the image from appropriate path
image = img_as_float(
    io.imread('./Blender-Denoiser/noisy-img.png'))

# Display the image
cv2.imshow("Image", image)

# Apply shift-invariant wavelet denoising
# Sigma is the noise standard deviation
# Uses cycle-spinning to perform shift-invariance
def wavelet_dn(image):
    sigma = 0.01
    image = image + sigma * np.random.standard_normal(image.shape)
    filtered_image = cycle_spin(image, func=denoise_wavelet,
                                max_shifts=5)
    return filtered_image


# Display the filtered image
cv2.imshow('Filtered Image', wavelet_dn(image))
cv2.waitKey(0)  # Wait for a key press to exit
cv2.destroyAllWindows()  # Close all windows
