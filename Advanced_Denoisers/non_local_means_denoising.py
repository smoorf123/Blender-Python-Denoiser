import cv2 

# Apply non-local means denoising, 10 filter strength, 10 filter strength
# of color components, 7 size of template patch used to compute weights,
# 21 size of window used to compute weighted average
def nlm_dn(image):
    img = cv2.imread(image)
    filtered_image = cv2.fastNlMeansDenoisingColored(img, None, 12, 12, 7, 21)
    return filtered_image
