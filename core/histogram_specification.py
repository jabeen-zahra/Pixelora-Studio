"""
Histogram Specification — implemented exactly as we studied algorithm in lecture:

    1. Specify the desired (reference) histogram.
    2. Build Mapping Table 1: histogram-equalize the SOURCE image
       (running sum -> normalize -> multiply by max gray level -> round).
    3. Build Mapping Table 2: histogram-equalize the REFERENCE histogram
       with the same four steps.
    4. Combine Table 1 and Table 2: for every source gray level, take its
       equalized value (from Table 1) and find the reference gray level
       whose equalized value (from Table 2) is the closest match.
    5. Apply that final mapping to every pixel of the source image.

No built-in histogram / equalization functions are used anywhere.
"""

MAX_GRAY_LEVEL = 255  # 8-bit images: levels 0-255


# ----------------------------------------------------------------------
# Building block 1: raw histogram
# ----------------------------------------------------------------------
def calculate_histogram(image):
    """Count how many pixels fall at each gray level (0-255)."""
    height = len(image)
    width = len(image[0])
    histogram = [0] * 256

    for y in range(height):
        for x in range(width):
            pixel = int(image[y][x])
            histogram[pixel] += 1

    return histogram


# ----------------------------------------------------------------------
# Equalization step 1: running sum of the histogram
# ----------------------------------------------------------------------
def calculate_running_sum(histogram):
    cumulative = []
    total = 0

    for count in histogram:
        total += count
        cumulative.append(total)

    return cumulative


# ----------------------------------------------------------------------
# Equalization step 2: normalize by total pixel count
# ----------------------------------------------------------------------
def normalize_running_sum(running_sum, total_pixels):
    normalized = []

    for value in running_sum:
        normalized.append(value / total_pixels)

    return normalized


# ----------------------------------------------------------------------
# Equalization steps 3 & 4: scale by max gray level,
# round, and read off the one-to-one mapping (index = original level,
# value = equalized level). This single array IS the mapping table.
# ----------------------------------------------------------------------
def scale_to_gray_levels(normalized, max_gray_level=MAX_GRAY_LEVEL):
    mapping_table = []

    for value in normalized:
        scaled = value * max_gray_level
        rounded = int(scaled + 0.5)  # manual round-off 
        if rounded > max_gray_level:
            rounded = max_gray_level
        mapping_table.append(rounded)

    return mapping_table


def equalize_histogram(histogram, total_pixels, max_gray_level=MAX_GRAY_LEVEL):
    """
    Runs the full 4-step equalization process from the slides and returns
    the resulting mapping table (Table 1 for the source, Table 2 for the
    reference, depending on what's passed in).
    """
    running_sum = calculate_running_sum(histogram)
    normalized = normalize_running_sum(running_sum, total_pixels)
    mapping_table = scale_to_gray_levels(normalized, max_gray_level)
    return mapping_table


# ----------------------------------------------------------------------
# Step 4: combine Table 1 and Table 2 into the final mapping M.
# For each source level O, look up its equalized value H = Table1[O],
# then search Table 2 for the reference level OS whose equalized value
# HS is closest to H.
# ----------------------------------------------------------------------
def create_specification_mapping(table1, table2):
    num_levels = len(table1)
    final_mapping = [0] * num_levels

    for o in range(num_levels):
        h = table1[o]

        best_os = 0
        smallest_difference = abs(h - table2[0])

        for os_level in range(1, num_levels):
            difference = abs(h - table2[os_level])
            if difference < smallest_difference:
                smallest_difference = difference
                best_os = os_level

        final_mapping[o] = best_os

    return final_mapping


# ----------------------------------------------------------------------
# Step 5: apply the final mapping to every pixel.
# ----------------------------------------------------------------------
def apply_mapping(image, mapping):
    height = len(image)
    width = len(image[0])
    output = []

    for y in range(height):
        row = []
        for x in range(width):
            pixel = int(image[y][x])
            row.append(mapping[pixel])
        output.append(row)

    return output


# ----------------------------------------------------------------------
# Orchestration
# ----------------------------------------------------------------------
def histogram_specification(source_image, reference_image):
    source_histogram = calculate_histogram(source_image)
    reference_histogram = calculate_histogram(reference_image)

    source_pixels = len(source_image) * len(source_image[0])
    reference_pixels = len(reference_image) * len(reference_image[0])

    # Mapping Table 1: equalize the source image
    table1 = equalize_histogram(source_histogram, source_pixels)

    # Mapping Table 2: equalize the specified/reference histogram
    table2 = equalize_histogram(reference_histogram, reference_pixels)

    # Final mapping table M
    mapping = create_specification_mapping(table1, table2)

    # Apply mapping to the source image
    output_image = apply_mapping(source_image, mapping)
    output_histogram = calculate_histogram(output_image)

    return {
        "source_histogram": source_histogram,
        "reference_histogram": reference_histogram,
        "output_histogram": output_histogram,
        "mapping": mapping,
        "output_image": output_image,
        "equalization_table_source": table1,
        "equalization_table_reference": table2,
    }