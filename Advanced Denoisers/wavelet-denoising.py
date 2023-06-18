import skimage.restoration as skr   # Import the scikit-image library
import cv2  # Import the OpenCV library

# Read the image from appropriate path
image = cv2.imread('./Blender-Denoiser/noisy-img.png')

# Display the image
cv2.imshow("Image", image)

# Apply wavelet denoising
# channel_axis specifies the axis of color channels with -1 being the last
# axis (color), convert2ycbcr converts the image to YCbCr color space
def wavelet_dn(image):
    filtered_image = skr.denoise_wavelet(image, 
                multichannel=True, convert2ycbcr=True)
    return filtered_image

# Display the filtered image
cv2.imshow('Filtered Image', wavelet_dn(image))
cv2.waitKey(0)  # Wait for a key press to exit
cv2.destroyAllWindows()  # Close all windows
