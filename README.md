# Blender Python Denoiser

![Blender version](https://img.shields.io/badge/Blender-2.80+-orange.svg)
![Addon version](https://img.shields.io/badge/Addon%20version-0.1-blue.svg)

The Blender Python Denoiser is an addon for Blender that provides a simple way to denoise your rendered images using Python scripting. It leverages standalone denoising algorithms, allowing users to select their preferred denoising method based on preference and performance.

## Features

-   Integration with standalone denoising algorithms.
-   Ability to choose denoising options through a user-friendly interface.
-   Choice between fast, traditional methods and more advanced algorithms using machine learning.

## Installation

1. Download the code in a ZIP format (Green "CODE" drop down).
2. Open Blender.
3. Go to `Edit` → `Preferences` → `Add-ons`.
4. Click on the `Install` button.
5. Navigate to the downloaded repository and select the ZIP file.
6. Enable the addon by checking the checkbox next to its name.

⚠️ **Warning**: Upon registration, the addon will automatically download the following Python libraries: bm3d, skimage, scipy, and opencv-python. Please ensure you have an active internet connection during installation.

## Usage

1. Open Blender.
2. Ensure that the addon is enabled (see the Installation section).
3. Setup your scene as preferred.
4. Press the `N` key to reveal the addons panel.
5. Expand the `Custom Denoiser` section.
6. Set save location first, on where you would like all renders AND denoised outputs to be saved.
7. Select desired denoising algorithm.
8. Click on the `Denoise Preview` button to apply denoising to the current rendered scene and just provide a preview (denoised image and render will not be saved).
9. Click on the `Denoise` when finally ready to preview and save both render and denoised version in location set in step 6.

## Denoiser Advice

Advanced Denoisers such as Bilateral, Non-Local Means, BM3D, Total-Variation and Wavelet denoising offer better quality denoising performance compared to Traditional Denoisers such as Gaussian, Mean and Median denoising. BM3D performs best in most cases.

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please feel free to open an issue or submit a pull request.

## License

This addon is licensed under the [MIT License](LICENSE).

## Acknowledgements

The Blender Python Denoiser addon was created by [Somil Varshney](https://github.com/smoorf123).

Special thanks to the Blender community for their valuable feedback and support.
