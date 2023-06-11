import cv2  # Import the OpenCV library

# Read the image from appropriate path
image = cv2.imread('./Blender-Denoiser/noisy-img.png')

# Display the image
cv2.imshow("Image", image)

# Apply gaussian filtering with a 5x5 kernel, 0 implying that the standard deviation is calculated automatically
filtered_image = cv2.GaussianBlur(image, (5, 5), 0)

# Display the filtered image
cv2.imshow('Filtered Image', filtered_image)
cv2.waitKey(0)  # Wait for a key press to exit
cv2.destroyAllWindows()  # Close all windows
