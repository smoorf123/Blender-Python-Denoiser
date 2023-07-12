import cv2 
import os

def denoise(FILE_PATH, FILE_PATH_DENOISED, function):
    image = cv2.imread(FILE_PATH)
    denoised_img = function(FILE_PATH)

    save_image(image, FILE_PATH)
    save_image(denoised_img, FILE_PATH_DENOISED)

def denoise_preview(FILE_PATH, function):
    # Display the filtered image
    cv2.imshow('Denoised Image', function(FILE_PATH))
    cv2.waitKey(0)  # Wait for a key press to exit
    cv2.destroyAllWindows()  # Close all windows
    remove_image(FILE_PATH)

def save_image(image, FILE_PATH):
    cv2.imwrite(FILE_PATH, image)
    print("Image saved!")

def remove_image(FILE_PATH):
    try:
        os.remove(FILE_PATH)
        print("Image removed!")
    except: pass