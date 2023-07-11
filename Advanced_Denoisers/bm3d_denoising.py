from bm3d import bm3d, BM3DStages
from skimage import img_as_float
import cv2

# Apply bm3d filtering
# sigma_psd is the noise standard deviation, ALL_STAGES implies hard thresholding
# and wiener filtering are both applied
def bm3d_dn(image):
    img = img_as_float(cv2.imread(image))
    filtered_image = bm3d(
        img, sigma_psd=0.1, stage_arg=BM3DStages.ALL_STAGES)
    return filtered_image