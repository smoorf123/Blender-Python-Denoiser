import bm3d  # Import the bm3d library
from skimage import io, img_as_float  # Import the scikit-image library

# Apply bm3d filtering
# sigma_psd is the noise standard deviation, ALL_STAGES implies hard thresholding
# and wiener filtering are both applied
def bm3d_dn(image):
    img = img_as_float(io.imread(image, as_gray=True))
    filtered_image = bm3d.bm3d(
        img, sigma_psd=0.1, stage_arg=bm3d.BM3DStages.ALL_STAGES)
    return filtered_image
