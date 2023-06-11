# Blender-Python-Denoiser

This project aims to build a Blender Plugin for a multi-algorithm based denoiser where users have the choice to select between various approaches to denoise their renders.

This includes all of the rendering options listed below:

## Smoothing Based Denoising

Testing out basic forms of filtering first, namely smoothing/blurring based filtering such as mean, median, gaussian and bilateral filtering.

### Mean Filtering

Mean filtering works by replacing each pixel's value with the average of its neighboring pixels.

Use cases for mean filtering:

-   Image denoising in scenarios where noise is relatively uniform across the image.
-   Pre-processing step for other image processing tasks like edge detection or segmentation.

### Median Filtering

Median filtering is a non-linear filtering method that replaces each pixel's value with the median of its neighboring pixels.

Use cases for median filtering:

-   Removing salt-and-pepper noise in images acquired from low-quality sensors or transmitted over noisy channels.
-   Pre-processing step for computer vision tasks like object detection or optical character recognition (OCR).

### Gaussian Filtering

Gaussian filtering applies a Gaussian kernel to an image, which is a weighted average of the neighboring pixels.

Use cases for Gaussian filtering:

-   Image smoothing and denoising, especially for images with a lot of Gaussian noise.
-   Pre-processing step for feature extraction or image enhancement algorithms.

### Bilateral Filtering

Bilateral filtering is a non-linear filtering technique that considers both spatial and intensity differences between pixels. It applies a weighted average to the neighboring pixels, where the weights depend on both the spatial distance and the intensity difference.

Use cases for bilateral filtering:

-   Image denoising while preserving sharp edges, suitable for images with complex textures or fine details.
-   Real-time image and video processing applications where noise reduction is required without sacrificing image quality.
