"""
BM3D is an algorithm for attenuation of additive spatially correlated
stationary (aka colored) Gaussian noise.

based on Y. Mäkinen, L. Azzari, A. Foi, 2020,
"Collaborative Filtering of Correlated Noise: Exact Transform-Domain Variance for Improved Shrinkage and Patch Matching"
in IEEE Transactions on Image Processing, vol. 29, pp. 8339-8354.

Copyright (c) 2006-2022 Tampere University.
All rights reserved.
This work (software, material, and documentation) shall only
be used for nonprofit noncommercial purposes.
Any unauthorized use of this work for commercial or for-profit purposes
is prohibited.
"""


import numpy as np
import copy
from typing import Union, Tuple
from scipy.fftpack import *
import bm4d as _bm4d

from .profiles import BM3DProfile, BM3DProfileRefilter, BM3DProfileVN, BM3DStages
from .profiles import BM3DProfileDeb, BM3DProfileHigh, BM3DProfileLC, BM3DProfileVNOld

EPS = 2.2204e-16


def bm3d_rgb(z: np.ndarray, sigma_psd: Union[np.ndarray, list, float],
             profile: Union[BM3DProfile, str] = 'np', colorspace: str = 'opp')\
        -> np.ndarray:
    """
    BM3D For color images. Performs color transform to do block-matching in luminance domain.
    :param z: Noisy image, 3 channels (MxNx3)
    :param sigma_psd: Noise PSD, either MxN or MxNx3 (different PSDs for different channels)
                        or
                      Noise standard deviation, either float, or [float, float, float] for 3 different stds.
    :param profile: Settings for BM3D: BM3DProfile object or a string.
                    ('np', 'refilter', 'vn', 'vn_old', 'high', 'deb')
    :param colorspace: 'YCbCr' or 'opp' for choosing the color transform
    :return: denoised color image, same size as z
    """

    # Forward color transform
    z, imax, imin, scale, a = rgb_to(z, colorspace)

    # Scale PSD appropriately

    # Multiple PSDs / sigmas

    if np.ndim(sigma_psd) == 1 or (np.ndim(sigma_psd) == 3 and sigma_psd.shape[2] == 3):
        sigma_psd = np.array(sigma_psd)
        if np.ndim(sigma_psd) == 3:
            o = sigma_psd.reshape([sigma_psd.shape[0] * sigma_psd.shape[1], 3]) @ (a.T ** 2)
            o = o.reshape([sigma_psd.shape[0], sigma_psd.shape[1], 3])
            sigma_psd = o / np.transpose(np.atleast_3d((imax - imin) ** 2), (0, 2, 1))
        else:
            # One-dim PSDs
            o = np.array(np.ravel(sigma_psd)).T ** 2 @ (a.T ** 2)
            sigma_psd = np.sqrt(o / (imax - imin) ** 2)
    else:
        if np.squeeze(sigma_psd).ndim <= 1:  # stds are scaled by the sqrt.
            sigma_psd = sigma_psd * np.transpose(np.atleast_3d(np.sqrt(scale)), (0, 2, 1))
        else:
            sigma_psd = np.atleast_3d(sigma_psd) * np.transpose(np.atleast_3d(scale), (0, 2, 1))

    # Call BM3D with the transformed image and PSD
    y_hat = bm3d(z, sigma_psd, profile)

    # Inverse transform to get the final estimate
    y_hat, imax, imin, scale, a = rgb_to(y_hat, colorspace, True, imax, imin)

    return y_hat


def bm3d_deblurring(z: np.ndarray,
                    sigma_psd: Union[np.ndarray, list, float],
                    psf: np.ndarray, profile: Union[BM3DProfile, str] = 'np')\
        -> np.ndarray:
    """
    BM3D Deblurring. Performs regularization, then denoising.
    :param z: Noisy blurred image. either MxN or MxNxC where C is the channel count.
    :param sigma_psd: Noise PSD, either MxN or MxNxC (different PSDs for different channels)
                        or
                      sigma_psd: Noise standard deviation, either float, or length C list of floats
    :param psf: Blur point-spread function in space domain.
    :param profile: Settings for BM3D: BM3DProfile object or a string.
                    ('np', 'refilter', 'vn', 'vn_old', 'high', 'deb')
    :return: denoised, deblurred image, same size as z
    """

    # Handle both PSDs and sigmas
    sigma_psd = np.array(sigma_psd)

    # Create big PSD
    if np.squeeze(sigma_psd).ndim <= 1:
        sigma_psd = np.ones(z.shape) * np.ravel(sigma_psd ** 2).reshape([1, 1, np.size(sigma_psd)]) * \
                    z.shape[0] * z.shape[1]

    sigma_psd = np.atleast_3d(sigma_psd)
    z = np.atleast_3d(z)

    # Regularized inverse
    regularization_alpha_ri = 4e-4

    # pad PSF with zeros to whole image domain, and center it
    big_v = np.zeros(z.shape[0:2])
    big_v[0:psf.shape[0], 0:psf.shape[1]] = psf
    big_v = np.roll(big_v, -np.array(np.round([(psf.shape[0] - 1) / 2,
                                               (psf.shape[1] - 1) / 2]), dtype=int), axis=(0, 1))

    # PSF in FFT
    fft_v = np.atleast_3d(fft2(big_v, axes=(0, 1)))

    # Standard Tikhonov Regularization
    regularized_inverse = np.conj(fft_v) / ((np.abs(fft_v) ** 2) + regularization_alpha_ri * sigma_psd + EPS)

    # Regularized Inverse Estimate (RI OBSERVATION)
    z_ri = np.real(ifft2(fft2(z, axes=(0, 1)) * regularized_inverse, axes=(0, 1)))

    # PSD of estimate
    sigma_psd_ri = sigma_psd * abs(regularized_inverse) ** 2

    # Call BM3D hard-thresholding with the RI and its PSD
    y_hat = bm3d(z_ri, sigma_psd_ri, profile, stage_arg=BM3DStages.HARD_THRESHOLDING)

    # Regularized Wiener Inversion
    regularization_alpha_rwi = 5e-3

    # Wiener reference estimate
    wiener_pilot = np.atleast_3d(abs(fft2(y_hat, axes=(0, 1))))

    # Transfer Matrix for RWI(uses standard regularization 'a-la-Tikhonov')
    regularized_wiener_inverse = (np.conj(fft_v) * wiener_pilot ** 2) / (wiener_pilot ** 2 * (np.abs(fft_v) ** 2) +
                                                                         regularization_alpha_rwi * sigma_psd + EPS)

    # Regularized Wiener inverse
    z_rwi = np.real(ifft2(fft2(z, axes=(0, 1)) * regularized_wiener_inverse, axes=(0, 1)))
    # And its PSD
    sigma_psd_rwi = sigma_psd * np.abs(regularized_wiener_inverse) ** 2

    # Filter zRWI in Wiener using the HT result as pilot
    return bm3d(z_rwi, sigma_psd_rwi, profile, stage_arg=y_hat)


def bm3d(z: np.ndarray, sigma_psd: Union[np.ndarray, list, float],
         profile: Union[BM3DProfile, str] = 'np',
         stage_arg: Union[BM3DStages, np.ndarray] = BM3DStages.ALL_STAGES,
         blockmatches: tuple = (False, False))\
        -> Union[np.ndarray, Tuple[np.ndarray, Tuple[np.ndarray, np.ndarray]]]:
    """
    Perform BM3D denoising on z: either hard-thresholding, Wiener filtering or both.

    :param z: Noisy image. either MxN or MxNxC where C is the channel count.
              For multichannel images, blockmatching is performed on the first channel.
    :param sigma_psd: Noise PSD, either MxN or MxNxC (different PSDs for different channels)
            or
           sigma_psd: Noise standard deviation, either float, or length C list of floats
    :param profile: Settings for BM3D: BM3DProfile object or a string
                    ('np', 'refilter', 'vn', 'vn_old', 'high', 'deb'). Default 'np'.
    :param stage_arg: Determines whether to perform hard-thresholding or wiener filtering.
                    either BM3DStages.HARD_THRESHOLDING, BM3DStages.ALL_STAGES or an estimate
                    of the noise-free image.
                    - BM3DStages.ALL_STAGES: Perform both.
                    - BM3DStages.HARD_THRESHOLDING: Perform hard-thresholding only.
                    - ndarray, size of z: Perform Wiener Filtering with stage_arg as pilot.
    :param blockmatches: Tuple (HT, Wiener), with either value either:
                        - False : Do not save blockmatches for phase
                        - True : Save blockmatches for phase
                        - Pre-computed block-matching array returned by a previous call with [True]
                        Such as y_est, matches = bm3d(z, sigma_psd, profile, blockMatches=(True, True))
                        y_est2 = bm3d(z2, sigma_psd, profile, blockMatches=matches);
                        Note that saved values are not necessarily compatible between library versions.
    :return:
        - denoised image, same size as z: if blockmatches == (False, False)
        - denoised image, blockmatch data: if either element of blockmatches is True
    """

    # Profile selection, if profile is a string, otherwise BM3DProfile.
    pro = _select_profile(profile)

    # Ensure z is 3-D a numpy array
    z = np.array(z)
    if z.ndim != 2 and z.ndim != 3:
        raise ValueError("z must be either 2D or 3D!")
    if z.ndim == 2:
        z = np.atleast_3d(z)

    channel_count = z.shape[2]
    sigma_psd = np.array(sigma_psd)

    converted_profile = _convert_profile(pro)

    blockmatches_ht, blockmatches_wie = blockmatches  # Break apart
    incl_blockmatches = (blockmatches_ht is True) or \
                        (blockmatches_wie is True)

    bm = 0

    if channel_count > 1:  # Multichannel BM3D
        if blockmatches_ht or blockmatches_wie:
            print("Warning: passed blockmatches argument with multichannel call, "
                  "having no effect. Call the function separately for each channel!")

        # Format PSDs so that the list dimension is 4th, not 3rd
        if np.squeeze(sigma_psd).ndim == 1:  # list of stds
            sigma_psd = np.array([np.atleast_3d(np.ravel(sigma_psd))]).transpose((2, 0, 1, 3))
        elif sigma_psd.ndim == 3:  # List of full PSDs
            sigma_psd = np.array([sigma_psd]).transpose((3, 1, 2, 0))
        elif sigma_psd.ndim == 2:
            sigma_psd = np.array([[sigma_psd]]).transpose((0, 2, 3, 1))
        z = np.array([z]).transpose((3, 1, 2, 0))
        y_hat = _bm4d.bm4d_multichannel(z, sigma_psd, converted_profile, stage_arg)
    else:
        if incl_blockmatches:
            y_hat, bm = _bm4d.bm4d(z, sigma_psd, converted_profile, stage_arg, blockmatches)
        else:
            y_hat = _bm4d.bm4d(z, sigma_psd, converted_profile, stage_arg, blockmatches)

    # Remove useless dimension if only single output
    if channel_count == 1:
        y_hat = y_hat[:, :, 0]
    else:
        y_hat = y_hat[:, :, :, 0].transpose((1, 2, 0))
    if incl_blockmatches:
        return y_hat, bm

    return y_hat


def _convert_profile(pro_in: BM3DProfile) -> _bm4d.BM4DProfile:
    pro = _bm4d.BM4DProfileBM3D()

    pro.filter_strength = pro_in.filter_strength

    pro.print_info = pro_in.print_info

    pro.transform_local_ht_name = pro_in.transform_2d_ht_name
    pro.transform_local_wiener_name = pro_in.transform_2d_wiener_name
    pro.transform_nonlocal_name = pro_in.transform_3rd_dim_name

    pro.nf = (pro_in.nf, pro_in.nf, 1)
    pro.k = pro_in.k

    pro.denoise_residual = pro_in.denoise_residual
    pro.residual_thr = pro_in.residual_thr
    pro.max_pad_size = pro_in.max_pad_size

    pro.gamma = pro_in.gamma

    pro.bs_ht = (pro_in.bs_ht, pro_in.bs_ht, 1)
    pro.step_ht = (pro_in.step_ht, pro_in.step_ht, 1)

    pro.max_stack_size_ht = pro_in.max_3d_size_ht
    pro.search_window_ht = (pro_in.search_window_ht // 2, pro_in.search_window_ht // 2, 1)
    pro.tau_match = pro_in.tau_match * pro_in.bs_ht ** 2 / 255 ** 2

    pro.lambda_thr = pro_in.lambda_thr3d
    pro.mu2 = pro_in.mu2

    pro.lambda_thr_re = pro_in.lambda_thr3d_re
    pro.mu2_re = pro_in.mu2_re
    pro.beta = pro_in.beta

    pro.bs_wiener = (pro_in.bs_wiener, pro_in.bs_wiener, 1)
    pro.step_wiener = (pro_in.step_wiener, pro_in.step_wiener, 1)

    pro.max_stack_size_wiener = pro_in.max_3d_size_wiener
    pro.search_window_wiener = (pro_in.search_window_wiener // 2, pro_in.search_window_wiener // 2, 1)
    pro.tau_match_wiener = pro_in.tau_match_wiener * pro_in.bs_wiener ** 2 / 255 ** 2
    pro.beta_wiener = pro_in.beta_wiener
    pro.dec_level = pro_in.dec_level

    pro.set_sharpen(pro_in.sharpen_alpha)
    pro.num_threads = pro_in.num_threads

    return pro


def gaussian_kernel(size: tuple, std: float, std2: float = -1) -> np.ndarray:
    """
    Get a 2D Gaussian kernel of size (sz1, sz2) with the specified standard deviations.
    If std2 is not specified, both stds will be the same.
    :param size: kernel size, tuple
    :param std: std of 1st dimension
    :param std2: std of 2nd dimension, or -1 if equal to std
    :return: normalized Gaussian kernel (sum == 1)
    """
    return _bm4d.gaussian_kernel(size, std, std2)


def _select_profile(profile: Union[str, BM3DProfile]) -> BM3DProfile:
    """
    Select profile for BM3D
    :param profile: BM3DProfile or a string
    :return: BM3DProfile object
    """
    if isinstance(profile, BM3DProfile):
        pro = copy.copy(profile)
    elif profile == 'np':
        pro = BM3DProfile()
    elif profile == 'refilter':
        pro = BM3DProfileRefilter()
    elif profile == 'vn':
        pro = BM3DProfileVN()
    elif profile == 'high':
        pro = BM3DProfileHigh()
    elif profile == 'vn_old':
        pro = BM3DProfileVNOld()
    elif profile == 'deb':
        pro = BM3DProfileDeb()
    else:
        raise TypeError('"profile" should be either a string of '
                        '"np"/"refilter"/"vn"/"high"/"vn_old"/"deb" or a BM3DProfile object!')
    return pro


def rgb_to(img: np.ndarray, colormode: str = 'YCbCr', inverse: bool = False,
           o_max: float = 0, o_min: float = 0)\
        -> (np.ndarray, float, float, float, np.ndarray):
    """
    Converts to normalized YCbCr or 'opp' (or back), returns normalization values needed for inverse
    :param img: image to transform (MxNx3)
    :param colormode: 'YCbCr' or 'opp'
    :param inverse: if True, do the inverse instead
    :param o_max: max value used for inverse scaling (returned by forward)
    :param o_min: min value used for inverse scaling (returned by forward)
    :return: (normalized+transformed image, o_max, o_min, scale used to multiply 1-D PSD, forward transform used)
    """
    if colormode == 'opp':
        # Forward
        a = np.array([[1/3, 1/3, 1/3], [0.5, 0, -0.5], [0.25, -0.5, 0.25]])
        # Inverse
        b = np.array([[1, 1, 2/3], [1, 0, -4/3], [1, -1, 2/3]])
    else:
        # YCbCr
        a = np.array([[0.299, 0.587, 0.114], [-0.168737, -0.331263, 0.5], [0.5, -0.418688, -0.081313]])
        b = np.array([[1.0000, 0.0000, 1.4020], [1.0000, -0.3441, -0.7141], [1.0000, 1.7720, 0.0000]])

    if inverse:
        # The inverse transform
        o = (img.reshape([img.shape[0] * img.shape[1], 3]) * (o_max - o_min) + o_min) @ b.T
        scale = None
    else:
        # The color transform
        o = img.reshape([img.shape[0] * img.shape[1], 3]) @ a.T
        o_max = np.max(o, axis=0)
        o_min = np.min(o, axis=0)
        o = (o - o_min) / (o_max - o_min)
        scale = np.sum(a.T ** 2, axis=0) / (o_max - o_min) ** 2

    return o.reshape([img.shape[0], img.shape[1], 3]), o_max, o_min, scale, a

