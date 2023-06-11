import cv2  # Import the OpenCV library
import bm3d  # Import the bm3d library
from skimage import io, img_as_float  # Import the scikit-image library

# Read the image from appropriate path and convert it to float for bm3d processing
image = img_as_float(
    io.imread('./Blender-Denoiser/noisy-img.png', as_gray=True))

# Display the image
cv2.imshow("Image", image)

# Apply bm3d filtering
# sigma_psd is the noise standard deviation, ALL_STAGES implies hard thresholding and wiener filtering are both applied
filtered_image = bm3d.bm3d(
    image, sigma_psd=0.1, stage_arg=bm3d.BM3DStages.ALL_STAGES)

# Display the filtered image
cv2.imshow('Filtered Image', filtered_image)
cv2.waitKey(0)  # Wait for a key press to exit
cv2.destroyAllWindows()  # Close all windows
