import sys
sys.path.insert(0, "C:/Users/Somil/Desktop/VSCode-Python/Blender-Denoiser/Required_Dependencies/cv2")

from cv2 import imread, fastNlMeansDenoisingColored  

# Apply non-local means denoising, 10 filter strength, 10 filter strength
# of color components, 7 size of template patch used to compute weights,
# 21 size of window used to compute weighted average
def nlm_dn(image):
    img = imread(image)
    filtered_image = fastNlMeansDenoisingColored(img, None, 12, 12, 7, 21)
    return filtered_image
