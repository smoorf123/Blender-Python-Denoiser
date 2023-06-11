import cv2  # Import the OpenCV library

# Read the image from appropriate path
image = cv2.imread('./Blender-Denoiser/noisy-img.png')

# Display the image
cv2.imshow("Image", image)

# Apply bilateral filtering
# 9 is the diameter of the pixel neighborhood used, 75 is the sigma value for color space, 75 is the sigma value for coordinate space
filtered_image = cv2.bilateralFilter(image, 9, 75, 75)

# Display the filtered image
cv2.imshow('Filtered Image', filtered_image)
cv2.waitKey(0)  # Wait for a key press to exit
cv2.destroyAllWindows()  # Close all windows
