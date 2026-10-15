"""
Adaptive Contrast Enhancement (ACE) filter -- implemented exactly per the
lecture-slide formula:

    E(r,c) = k1 * [ M / sigma_i(r,c) ] * [ I(r,c) - m_i(r,c) ] + k2 * m_i(r,c)

Where:
    M            = the mean (average) for the ENTIRE image I(r,c)      [global, constant]
    sigma_i(r,c) = local standard deviation in the current n x n window
                   = sqrt( sum( (I(r,c) - m_i)^2 ) / (n^2 - 1) )
    m_i(r,c)     = local mean in the current window
    k1           = local gain factor constant, between 0 and 1
    k2           = local mean constant, between 0 and 1

The image is processed using the sliding-window concept (Figure 8.2-19):
the window is moved one pixel at a time across the image, and the outer
rows/columns that the window cannot fully cover are left unprocessed
(copied through unchanged), exactly as described in the slides.

No built-in mean/std/filter functions are used -- everything is computed
manually with explicit loops over the window.
"""


def calculate_global_mean(image):
    """Mean (average) gray value over the ENTIRE image -- this is M in the formula."""
    total = 0
    count = 0

    for row in image:
        for pixel in row:
            total += pixel
            count += 1

    return total / count


def _collect_window_pixels(image, r, c, half_window):
    """All pixel values inside the n x n window centered at (r, c)."""
    pixels = []

    for i in range(r - half_window, r + half_window + 1):
        for j in range(c - half_window, c + half_window + 1):
            pixels.append(image[i][j])

    return pixels


def calculate_local_mean(window_pixels):
    """m_i(r,c): mean of the pixels inside the current window."""
    return sum(window_pixels) / len(window_pixels)


def calculate_local_std(window_pixels, local_mean):
    """sigma_i(r,c): local standard deviation, using the n^2 - 1 denominator
    given in the slide formula."""
    n_squared = len(window_pixels)

    sum_of_squares = 0
    for pixel in window_pixels:
        sum_of_squares += (pixel - local_mean) ** 2

    denominator = n_squared - 1
    if denominator <= 0:
        denominator = 1  # guards the degenerate 1x1 window case

    return (sum_of_squares / denominator) ** 0.5


def apply_ace_filter(image, window_size=3, k1=0.5, k2=0.5):
    """
    Runs the ACE filter over the whole image using a sliding n x n window.

    Returns the enhanced image as a list of lists (same dimensions as the
    input). Border pixels that the window can't fully cover are copied
    through unchanged, matching the "unprocessed outer rows and columns"
    behaviour shown in the slides.
    """
    height = len(image)
    width = len(image[0])
    half_window = window_size // 2

    global_mean = calculate_global_mean(image)

    # start as a copy so the unprocessed border pixels are already correct
    output = [row[:] for row in image]

    for r in range(half_window, height - half_window):
        for c in range(half_window, width - half_window):
            window_pixels = _collect_window_pixels(image, r, c, half_window)
            local_mean = calculate_local_mean(window_pixels)
            local_std = calculate_local_std(window_pixels, local_mean)

            if local_std == 0:
                local_std = 1e-6  # avoid division by zero in perfectly flat regions

            gain = k1 * (global_mean / local_std)
            enhanced_value = gain * (image[r][c] - local_mean) + k2 * local_mean

            # clip to the valid 8-bit gray range
            if enhanced_value < 0:
                enhanced_value = 0
            elif enhanced_value > 255:
                enhanced_value = 255

            output[r][c] = int(enhanced_value + 0.5)

    return output


def histogram_stretch(image):
    """
    Simple linear contrast (histogram) stretch to the full 0-255 range.
    Used as the optional postprocessing step the slides pair with ACE
    results ("ACE filter results followed by a histogram stretch").
    """
    min_value = image[0][0]
    max_value = image[0][0]

    for row in image:
        for pixel in row:
            if pixel < min_value:
                min_value = pixel
            if pixel > max_value:
                max_value = pixel

    value_range = max_value - min_value
    if value_range == 0:
        return [row[:] for row in image]

    stretched = []
    for row in image:
        new_row = []
        for pixel in row:
            scaled = (pixel - min_value) / value_range * 255
            new_row.append(int(scaled + 0.5))
        stretched.append(new_row)

    return stretched


def ace_filter(image, window_size=3, k1=0.5, k2=0.5, apply_stretch=True):
    """
    Orchestrates the full ACE pipeline and returns everything the UI needs.
    """
    enhanced = apply_ace_filter(image, window_size=window_size, k1=k1, k2=k2)

    if apply_stretch:
        final_image = histogram_stretch(enhanced)
    else:
        final_image = enhanced

    return {
        "output_image": final_image,
        "window_size": window_size,
        "k1": k1,
        "k2": k2,
        "stretch_applied": apply_stretch,
    }
