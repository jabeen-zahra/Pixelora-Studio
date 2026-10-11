
def calculate_histogram(image):
    height = len(image)
    width = len(image[0])
    histogram = [0] * 256

    for y in range(height):
        for x in range(width):
            pixel = int(image[y][x])
            histogram[pixel] += 1

    return histogram


def calculate_cdf(histogram):
    cumulative = []
    total = 0

    for count in histogram:
        total += count
        cumulative.append(total)

    return cumulative


def normalize_cdf(cumulative, total_pixels):
    normalized = []

    for value in cumulative:
        normalized.append(value / total_pixels)

    return normalized


def create_mapping(source_cdf, reference_cdf):
    mapping = [0] * 256

    for i in range(256):
        best_level = 0
        smallest_difference = abs(source_cdf[i] - reference_cdf[0])

        for j in range(1, 256):
            difference = abs(source_cdf[i] - reference_cdf[j])

            if difference < smallest_difference:
                smallest_difference = difference
                best_level = j

        mapping[i] = best_level

    return mapping


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


def histogram_specification(source_image, reference_image):
    source_histogram = calculate_histogram(source_image)
    reference_histogram = calculate_histogram(reference_image)

    source_pixels = len(source_image) * len(source_image[0])
    reference_pixels = len(reference_image) * len(reference_image[0])

    source_cumulative = calculate_cdf(source_histogram)
    reference_cumulative = calculate_cdf(reference_histogram)

    source_cdf = normalize_cdf(source_cumulative, source_pixels)
    reference_cdf = normalize_cdf(reference_cumulative, reference_pixels)

    mapping = create_mapping(source_cdf, reference_cdf)
    output_image = apply_mapping(source_image, mapping)
    output_histogram = calculate_histogram(output_image)

    return {
        "source_histogram": source_histogram,
        "reference_histogram": reference_histogram,
        "output_histogram": output_histogram,
        "mapping": mapping,
        "output_image": output_image
    }
