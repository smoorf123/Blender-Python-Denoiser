import sys
sys.path.insert(0, "C:/Users/Somil/Desktop/VSCode-Python/Blender-Denoiser/Required_Dependencies/cv2")

import cv2

def denoise(FILE_PATH, FILE_PATH_DENOISED, function):
    image = cv2.imread(FILE_PATH)

    denoised_img = function(image)

    save_image(image, FILE_PATH)
    save_image(denoised_img, FILE_PATH_DENOISED)

def denoise_preview(FILE_PATH, function):
    image = cv2.imread(FILE_PATH)

    # Display the filtered image
    cv2.imshow('Filtered Image', function(image))
    cv2.waitKey(0)  # Wait for a key press to exit
    cv2.destroyAllWindows()  # Close all windows

def save_image(image, FILE_PATH):
    cv2.imwrite(FILE_PATH, image)
    print("Image saved!")
