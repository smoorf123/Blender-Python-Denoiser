import sys
sys.path.insert(0, "C:/Users/Somil/Desktop/VSCode-Python/Blender-Denoiser/Required_Dependencies/skimage")

from skimage.restoration import denoise_wavelet, cycle_spin
from skimage import io, img_as_float
import numpy as np

# Apply shift-invariant wavelet denoising
# Sigma is the noise standard deviation
# Uses cycle-spinning to perform shift-invariance
def wavelet_dn(image):
    img = img_as_float(io.imread(image))
    sigma = 0.01
    img = img + sigma * np.random.standard_normal(image.shape)
    filtered_image = cycle_spin(img, func=denoise_wavelet,
                                max_shifts=5)
    return filtered_image