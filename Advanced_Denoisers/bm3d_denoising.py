import sys
sys.path.insert(0, "C:/Users/Somil/Desktop/VSCode-Python/Blender-Denoiser/Required_Dependencies/bm3d")
sys.path.insert(0, "C:/Users/Somil/Desktop/VSCode-Python/Blender-Denoiser/Required_Dependencies/skimage")

from bm3d import bm3d, BM3DStages
from skimage import io, img_as_float

# Apply bm3d filtering
# sigma_psd is the noise standard deviation, ALL_STAGES implies hard thresholding
# and wiener filtering are both applied
def bm3d_dn(image):
    img = img_as_float(io.imread(image, as_gray=True))
    filtered_image = bm3d(
        img, sigma_psd=0.1, stage_arg=BM3DStages.ALL_STAGES)
    return filtered_image
