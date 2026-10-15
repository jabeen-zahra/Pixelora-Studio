"""
Pseudocolor in the Frequency Domain -- implemented per the lecture-slide
algorithm (Figure 8.2-26):

    1. Perform a Fourier transform on the image.
    2. Apply a lowpass, bandpass, and highpass filter to the transformed data.
    3. Perform an inverse Fourier transform on the three filter results.
    4. Use the three resulting images for the red, green, and blue color bands.

The three filters are ideal circular filters built from two user-chosen
cutoff frequencies (f_low < f_high), dividing the ENTIRE frequency domain
into three non-overlapping bands:

    Lowpass  : distance from the origin <= f_low
    Bandpass : f_low < distance from the origin <= f_high
    Highpass : distance from the origin >  f_high

numpy's FFT is used to perform the Fourier/inverse-Fourier transform itself
(implementing the FFT algorithm from scratch is a separate topic). The
optional histogram-equalization postprocessing step, however, reuses the
project's own manual histogram-equalization LUT from
core/histogram_specification.py -- no built-in histogram function is used
there either.
"""

import numpy as np

from core.histogram_specification import calculate_histogram, equalize_histogram

BAND_NAMES = ("lowpass", "bandpass", "highpass")


def compute_centered_fft(image):
    """Step 1: 2D Fourier transform, shifted so the zero frequency sits at the center."""
    image_array = np.array(image, dtype=np.float64)
    fft_result = np.fft.fft2(image_array)
    return np.fft.fftshift(fft_result)


def _distance_grid(height, width):
    """Distance of every frequency-domain coordinate from the center (the origin)."""
    center_r = height // 2
    center_c = width // 2

    rows = np.arange(height).reshape(-1, 1)
    cols = np.arange(width).reshape(1, -1)

    return np.sqrt((rows - center_r) ** 2 + (cols - center_c) ** 2)


def build_band_masks(height, width, cutoff_low, cutoff_high):
    """The three ideal masks (lowpass / bandpass / highpass) covering the
    whole frequency domain between them, per the slide's Figure 8.2-26(b)."""
    distance = _distance_grid(height, width)

    lowpass_mask = distance <= cutoff_low
    bandpass_mask = (distance > cutoff_low) & (distance <= cutoff_high)
    highpass_mask = distance > cutoff_high

    return {
        "lowpass": lowpass_mask,
        "bandpass": bandpass_mask,
        "highpass": highpass_mask,
    }


def apply_mask_and_inverse(fft_shifted, mask):
    """Steps 2 & 3: apply one band's mask, then inverse Fourier transform
    back to the spatial domain."""
    filtered = fft_shifted * mask
    unshifted = np.fft.ifftshift(filtered)
    spatial = np.fft.ifft2(unshifted)
    return np.abs(spatial)


def normalize_to_gray_levels(channel):
    """Manual min-max normalization of a filtered band result to 0-255."""
    min_val = float(channel.min())
    max_val = float(channel.max())

    if max_val - min_val == 0:
        return np.zeros_like(channel, dtype=np.uint8)

    stretched = (channel - min_val) / (max_val - min_val) * 255.0
    return stretched.astype(np.uint8)


def apply_histogram_equalization(channel_image_list):
    """Optional postprocessing step ("typical postprocessing includes
    histogram equalization"), reusing the project's own manual LUT builder."""
    histogram = calculate_histogram(channel_image_list)
    total_pixels = len(channel_image_list) * len(channel_image_list[0])
    lut = equalize_histogram(histogram, total_pixels, max_gray_level=255)

    output = []
    for row in channel_image_list:
        new_row = [lut[pixel] for pixel in row]
        output.append(new_row)

    return output


def pseudocolor_frequency_domain(image, cutoff_low, cutoff_high, channel_assignment, equalize=False):
    """
    channel_assignment: dict like {"R": "lowpass", "G": "bandpass", "B": "highpass"}
    -- must be a one-to-one assignment covering all three bands.

    Returns the three individual band results (as grayscale preview arrays)
    plus the final composed RGB pseudocolor image (step 4).
    """
    height = len(image)
    width = len(image[0])

    fft_shifted = compute_centered_fft(image)  # step 1
    masks = build_band_masks(height, width, cutoff_low, cutoff_high)  # step 2 setup

    band_results = {}
    for band_name in BAND_NAMES:
        spatial_result = apply_mask_and_inverse(fft_shifted, masks[band_name])  # steps 2 & 3
        band_results[band_name] = normalize_to_gray_levels(spatial_result)

    # step 4: assemble R, G, B from the three band results per the user's choice
    channels = {}
    for color_band in ("R", "G", "B"):
        band_name = channel_assignment[color_band]
        band_list = band_results[band_name].tolist()

        if equalize:
            band_list = apply_histogram_equalization(band_list)

        channels[color_band] = np.array(band_list, dtype=np.uint8)

    rgb_image = np.stack([channels["R"], channels["G"], channels["B"]], axis=-1)

    return {
        "lowpass_image": band_results["lowpass"],
        "bandpass_image": band_results["bandpass"],
        "highpass_image": band_results["highpass"],
        "rgb_image": rgb_image,
        "cutoff_low": cutoff_low,
        "cutoff_high": cutoff_high,
        "channel_assignment": channel_assignment,
        "equalize_applied": equalize,
    }
