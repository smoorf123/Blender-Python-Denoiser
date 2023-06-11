import cv2  # Import the OpenCV library

# Read the image from appropriate path
image = cv2.imread('./Blender-Denoiser/noisy-img.png')

# Display the image
cv2.imshow("Image", image)

# Apply non-local means denoising, 10 filter strength, 10 filter strength of color components, 7 size of template patch used to compute weights, 21 size of window used to compute weighted average
filtered_image = cv2.fastNlMeansDenoisingColored(image, None, 12, 12, 7, 21)

# Display the filtered image
cv2.imshow('Filtered Image', filtered_image)
cv2.waitKey(0)  # Wait for a key press to exit
cv2.destroyAllWindows()  # Close all windows
