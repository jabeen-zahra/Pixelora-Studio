<div align="center">

<img src="https://api.iconify.design/lucide:image.svg?color=%23ff8a3d" width="48"/>

# Pixelora Studio

**A growing suite of Digital Image Processing tools, built with Streamlit.**

<p>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" />
  <img src="https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logo=plotly&logoColor=white" />
  <img src="https://img.shields.io/badge/Pillow-7C3AED?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
</p>

<p>
  <img src="https://img.shields.io/github/last-commit/jabeen-zahra/Pixelora-Studio?style=flat-square&color=ff8a3d" />
  <img src="https://img.shields.io/github/license/jabeen-zahra/Pixelora-Studio?style=flat-square&color=ff8a3d" />
  <img src="https://img.shields.io/badge/status-active%20development-3dd68c?style=flat-square" />
</p>

</div>

---

### <img src="https://api.iconify.design/lucide:book-open.svg?color=%23ff8a3d" width="20" valign="middle"/> About

Pixelora Studio is designed to grow into a full suite of image processing tools — the operations listed in the sidebar outline where the studio is headed. Implemented so far: **Histogram Specification**, **ACE Filter**, and **Pseudocolor in the Frequency Domain**.

---

## <img src="https://api.iconify.design/lucide:list.svg?color=%23ff8a3d" width="20" valign="middle"/> Table of Contents

- [Histogram Specification](#histogram-specification)
- [ACE Filter](#ace-filter)
- [Pseudocolor (Frequency Domain)](#pseudocolor-frequency-domain)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Docker (optional)](#docker-optional)
- [Algorithms](#algorithms)
- [Roadmap](#roadmap)

---

## <img src="https://api.iconify.design/lucide:target.svg?color=%23ff8a3d" width="20" valign="middle"/> Histogram Specification

Remaps the tonal distribution of a source image so its histogram matches a reference image, using cumulative-distribution mapping.

| | |
|:---:|:---|
| <img src="https://api.iconify.design/lucide:upload.svg?color=%23ff8a3d" width="18"/> | Upload original and reference images |
| <img src="https://api.iconify.design/lucide:circle.svg?color=%23ff8a3d" width="18"/> | Convert images to grayscale |
| <img src="https://api.iconify.design/lucide:bar-chart-3.svg?color=%23ff8a3d" width="18"/> | Calculate histograms manually |
| <img src="https://api.iconify.design/lucide:trending-up.svg?color=%23ff8a3d" width="18"/> | Calculate cumulative histograms and normalized CDFs |
| <img src="https://api.iconify.design/lucide:shuffle.svg?color=%23ff8a3d" width="18"/> | Generate a histogram specification mapping table |
| <img src="https://api.iconify.design/lucide:sliders-horizontal.svg?color=%23ff8a3d" width="18"/> | Transform the original image |
| <img src="https://api.iconify.design/lucide:bar-chart-2.svg?color=%23ff8a3d" width="18"/> | Compare original, reference, and output histograms |
| <img src="https://api.iconify.design/lucide:download.svg?color=%23ff8a3d" width="18"/> | Download the resulting image |

---

## <img src="https://api.iconify.design/lucide:contrast.svg?color=%23ff8a3d" width="20" valign="middle"/> ACE Filter

Adaptive Contrast Enhancement — boosts contrast differently across different regions of an image, based on each region's own local brightness and detail level, using a sliding window.

| | |
|:---:|:---|
| <img src="https://api.iconify.design/lucide:upload.svg?color=%23ff8a3d" width="18"/> | Upload an image |
| <img src="https://api.iconify.design/lucide:scan.svg?color=%23ff8a3d" width="18"/> | Choose a sliding window size (n × n) |
| <img src="https://api.iconify.design/lucide:sliders-horizontal.svg?color=%23ff8a3d" width="18"/> | Adjust the gain (k1) and local-mean (k2) constants |
| <img src="https://api.iconify.design/lucide:calculator.svg?color=%23ff8a3d" width="18"/> | Calculate global and local mean/standard-deviation manually |
| <img src="https://api.iconify.design/lucide:wand-2.svg?color=%23ff8a3d" width="18"/> | Optionally apply a histogram stretch afterward |
| <img src="https://api.iconify.design/lucide:bar-chart-2.svg?color=%23ff8a3d" width="18"/> | Compare original and enhanced histograms |
| <img src="https://api.iconify.design/lucide:download.svg?color=%23ff8a3d" width="18"/> | Download the resulting image |

---

## <img src="https://api.iconify.design/lucide:palette.svg?color=%23ff8a3d" width="20" valign="middle"/> Pseudocolor (Frequency Domain)

Turns a grayscale image into a false-color image by separating it into frequency bands and mapping each one to a different color channel.

| | |
|:---:|:---|
| <img src="https://api.iconify.design/lucide:upload.svg?color=%23ff8a3d" width="18"/> | Upload an image |
| <img src="https://api.iconify.design/lucide:waves.svg?color=%23ff8a3d" width="18"/> | Apply a Fourier transform |
| <img src="https://api.iconify.design/lucide:sliders-horizontal.svg?color=%23ff8a3d" width="18"/> | Choose two cutoff frequencies to split the spectrum into three bands |
| <img src="https://api.iconify.design/lucide:shuffle.svg?color=%23ff8a3d" width="18"/> | Assign lowpass, bandpass, and highpass results to red, green, and blue |
| <img src="https://api.iconify.design/lucide:wand-2.svg?color=%23ff8a3d" width="18"/> | Optionally apply histogram equalization to each band |
| <img src="https://api.iconify.design/lucide:download.svg?color=%23ff8a3d" width="18"/> | Download the resulting pseudocolor image |

---

## <img src="https://api.iconify.design/lucide:wrench.svg?color=%23ff8a3d" width="20" valign="middle"/> Tech Stack

<div align="center">

| Technology | Role |
|:---:|:---|
| <img src="https://skillicons.dev/icons?i=python" width="32"/> | Core language |
| <img src="https://skillicons.dev/icons?i=streamlit" width="32"/> | Web app framework & UI |
| <img src="https://img.shields.io/badge/-NumPy-013243?style=flat-square&logo=numpy&logoColor=white" /> | Array operations, pixel mapping & Fourier transforms |
| <img src="https://img.shields.io/badge/-Matplotlib-11557c?style=flat-square" /> | Histogram plotting |
| <img src="https://img.shields.io/badge/-Pillow-7C3AED?style=flat-square" /> | Image I/O |
| <img src="https://skillicons.dev/icons?i=docker" width="32"/> | Optional containerized deployment |

</div>

---

## <img src="https://api.iconify.design/lucide:rocket.svg?color=%23ff8a3d" width="20" valign="middle"/> Installation

**1. Clone the repository**

```bash
git clone https://github.com/jabeen-zahra/Pixelora-Studio.git
cd Pixelora-Studio
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Run the application**

```bash
streamlit run app.py
```

> If `streamlit` isn't recognized as a command on your system, run it as a Python module instead:
> ```bash
> python -m streamlit run app.py
> ```

**4.** Open the local URL displayed in the terminal.

---

## <img src="https://api.iconify.design/lucide:box.svg?color=%23ff8a3d" width="20" valign="middle"/> Docker (optional)

Prefer not to set up a local Python environment? Run it in a container instead.

```bash
docker build -t pixelora-studio .
docker run -p 8501:8501 pixelora-studio
```

Then open **http://localhost:8501** in your browser.

---

## <img src="https://api.iconify.design/lucide:settings.svg?color=%23ff8a3d" width="20" valign="middle"/> Algorithms

### Histogram Specification

```
Source Image ──┐
                ├─▶ Histogram ──▶ CDF ──┐
Reference Image ┘                       ├─▶ Mapping Table ──▶ Output Image
                 Histogram ──▶ CDF ─────┘
```

1. Calculate the original and reference histograms
2. Calculate their cumulative sums
3. Normalize the cumulative histograms
4. Create a mapping table by matching the normalized cumulative distributions
5. Apply the mapping to every pixel of the original image

> The core histogram calculations and pixel mapping are implemented **manually**, without built-in histogram matching functions.

### ACE Filter

```
Input Image ──▶ Global Mean ──┐
                               ├─▶ Sliding n×n Window ──▶ Local Mean & Std-Dev ──▶ Enhanced Pixel
                               └───────────────────────────────────────────────┘
```

1. Calculate the mean of the entire image (the global mean)
2. Slide an n × n window across the image
3. At each window position, calculate the local mean and local standard deviation
4. Combine the global mean, local mean, and local standard deviation to compute the enhanced pixel value
5. Optionally apply a histogram stretch to the result

> Border rows/columns the window can't fully cover are left unprocessed, and all statistics are computed manually with explicit loops.

### Pseudocolor (Frequency Domain)

```
Image ──▶ Fourier Transform ──┬─▶ Lowpass  ──▶ Inverse FT ──▶ Red
                               ├─▶ Bandpass ──▶ Inverse FT ──▶ Green
                               └─▶ Highpass ──▶ Inverse FT ──▶ Blue
```

1. Perform a Fourier transform on the image
2. Apply a lowpass, bandpass, and highpass filter to the transformed data, using two cutoff frequencies that divide the entire spectrum between them
3. Perform an inverse Fourier transform on each of the three filtered results
4. Use the three resulting images for the red, green, and blue color bands
5. Optionally apply histogram equalization to each band as postprocessing

---

## <img src="https://api.iconify.design/lucide:map.svg?color=%23ff8a3d" width="20" valign="middle"/> Roadmap

This project was built as a Digital Image Processing coursework series. The rest of the sidebar reflects where the studio is headed.

- [x] Histogram Specification
- [x] ACE Filter
- [x] Pseudocolor (Frequency Domain)
- [ ] Histogram Equalization
- [ ] Convolution
- [ ] Segmentation

---

<div align="center">

Made as part of a Digital Image Processing coursework series

</div>