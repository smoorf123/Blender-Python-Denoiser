from bm3d import bm3d_rgb
from skimage import img_as_float, img_as_ubyte
import cv2

# Apply bm3d filtering
# sigma_psd is the noise standard deviation, ALL_STAGES implies hard thresholding
# and wiener filtering are both applied
def bm3d_dn(image):
    img = img_as_float(cv2.imread(image))
    filtered_image = bm3d_rgb(img, sigma_psd = 0.02, colorspace='rgb')
    return img_as_ubyte(filtered_image) # convert to 8-bit image for display
