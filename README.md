
# Histogram Specification Studio

A Python image processing application that implements histogram specification using a reference image.

## Features

- Upload original and reference images
- Convert images to grayscale
- Calculate histograms manually
- Calculate cumulative histograms and normalized CDFs
- Generate a histogram specification mapping table
- Transform the original image
- Compare original, reference, and output histograms
- Download the resulting image
- Run the application using Docker

## Technologies

- Python
- Streamlit
- NumPy
- Matplotlib
- Pillow
- Docker

## Installation

Clone the repository:

```bash
git clone https://github.com/jabeen-zahra/Pixelora-Studio.git
cd Pixelora-Studio
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal.

## Docker

Build the image:

```bash
docker build -t histogram-studio .
```

Run the container:

```bash
docker run -p 8501:8501 histogram-studio
```

Open http://localhost:8501 in your browser.

## Algorithm

1. Calculate the original and reference histograms.
2. Calculate their cumulative sums.
3. Normalize the cumulative histograms.
4. Create a mapping table by matching the normalized cumulative distributions.
5. Apply the mapping to every pixel of the original image.

The core histogram calculations and pixel mapping are implemented manually without built-in histogram matching functions.
