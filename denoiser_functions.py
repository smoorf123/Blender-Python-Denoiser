import cv2 
import os

def denoise(FILE_PATH, FILE_PATH_DENOISED, function):
    denoised_img = function(FILE_PATH)

    cv2.imshow('Denoised Image', denoised_img)
    cv2.waitKey(0)  # Wait for a key press to exit
    cv2.destroyAllWindows()  # Close all windows
    
    save_image(denoised_img, FILE_PATH_DENOISED)

def denoise_preview(FILE_PATH, function):
    cv2.imshow('Denoised Image', function(FILE_PATH))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    remove_image(FILE_PATH)

def save_image(image, FILE_PATH):
    cv2.imwrite(FILE_PATH, image)
    print("Image saved!")

def remove_image(FILE_PATH):
    print("Removing image...")
    try:
        os.remove(FILE_PATH)
        print("Image removed!")
    except: print("Image not found! Not removed.")