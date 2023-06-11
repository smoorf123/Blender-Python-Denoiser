# Blender-Python-Denoiser

This project aims to build a Blender Plugin for a multi-algorithm based denoiser where users have the choice to select between various approaches to denoise their renders.

This includes all of the rendering options listed below:

## Traditional Denoising

Traditionaldenoising methods, such as mean filtering, Gaussian filtering, and median filtering, apply linear filters to achieve smoothing and noise reduction. These methods focus on local pixel neighborhoods and often result in a loss of finer details.

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

## Advanced Denoising Methods

Advanced denoising methods, such as bilateral denoising, total variation denoising, non-local means denoising, wavelet denoising, and BM3D denoising incorporate more complex algorithms that take into account additional factors such as patch similarity, transform domains, or non-local pixel relationships. These methods aim to preserve finer details and edges while effectively reducing noise.

### Bilateral Filtering

Bilateral filtering is a non-linear filtering technique that considers both spatial and intensity differences between pixels. It applies a weighted average to the neighboring pixels, where the weights depend on both the spatial distance and the intensity difference.

Use cases for bilateral filtering:

-   Image denoising while preserving sharp edges, suitable for images with complex textures or fine details.
-   Real-time image and video processing applications where noise reduction is required without sacrificing image quality.

### Total Variation Denoising

Total Variation Denoising (TVD) using split-Bregman optimization is an advanced denoising technique that aims to reduce noise in an image while preserving important structures and edges. It achieves this by minimizing the total variation of the image through an iterative optimization process.

The split-Bregman optimization is a specific algorithmic approach used to solve the TVD problem. It decomposes the optimization problem into multiple smaller sub-problems, making it computationally efficient and facilitating convergence.

Use cases for Total Variation Denoising using split-Bregman optimization include:

-   Image denoising while preserving sharp edges: TVD is particularly useful for images with complex textures or fine details where preserving sharp edges is crucial.

-   Real-time image and video processing: TVD using split-Bregman optimization can be applied in real-time scenarios where noise reduction is required without sacrificing image quality.
