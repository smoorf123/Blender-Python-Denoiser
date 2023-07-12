from skimage.restoration import denoise_wavelet, cycle_spin
from skimage import img_as_float
import cv2 

# Apply shift-invariant wavelet denoising
# Sigma is the noise standard deviation
# Uses cycle-spinning to perform shift-invariance
def wavelet_dn(image):
    img = img_as_float(cv2.imread(image))
    denoise_kwargs = dict(channel_axis=-1, wavelet='db1', mode='soft')

    filtered_image = cycle_spin(img, func=denoise_wavelet, max_shifts=5, channel_axis=-1, func_kw=denoise_kwargs, num_workers=1)
    return filtered_image