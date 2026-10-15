"""Pure image / data helpers -- no page layout or routing logic here."""

from io import BytesIO

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image


def load_image(file) -> np.ndarray:
    """Load an uploaded file as an 8-bit grayscale numpy array."""
    return np.array(Image.open(file).convert("L"), dtype=np.uint8)


def image_bytes(image: np.ndarray) -> bytes:
    """Encode a numpy image array (grayscale or RGB) as PNG bytes for download buttons."""
    buffer = BytesIO()
    Image.fromarray(image).save(buffer, format="PNG")
    return buffer.getvalue()


def fmt_bytes(n: int) -> str:
    """Human-readable file size, e.g. 147.3 KB."""
    if n < 1024:
        return f"{n} B"
    if n < 1024 * 1024:
        return f"{n/1024:.1f} KB"
    return f"{n/(1024*1024):.1f} MB"


def mapping_table_html(inputs, outputs) -> str:
    """Render a scrollable Input -> Output gray-level mapping table."""
    rows = "".join(
        f"<tr><td>{i}</td><td>{o}</td></tr>" for i, o in zip(inputs, outputs)
    )
    return f"""
    <div class="map-table-wrap">
        <table class="map-table">
            <thead><tr><th>Input</th><th>Output</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    """


def show_histogram(histogram, color: str = "#ff8a3d") -> None:
    """Render a 256-bin grayscale histogram styled to match the app theme."""
    fig, ax = plt.subplots(figsize=(6, 2.3))
    fig.patch.set_facecolor("#1c1c21")
    ax.set_facecolor("#1c1c21")

    ax.bar(range(256), histogram, width=1, color=color, alpha=0.95)
    ax.set_xlim(0, 255)
    ax.set_xlabel("Gray level", color="#8b8f9c", fontsize=10, fontfamily="monospace", labelpad=6)
    ax.set_ylabel("Pixel count", color="#8b8f9c", fontsize=10, fontfamily="monospace", labelpad=6)
    ax.tick_params(colors="#8b8f9c", labelsize=9.5)
    ax.grid(axis="y", alpha=0.08, color="#ffffff", linewidth=0.6)

    for spine in ax.spines.values():
        spine.set_color("#2e2e36")
        spine.set_linewidth(0.9)

    fig.tight_layout(pad=0.8)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def calculate_histogram_for_display(image_list):
    """Lightweight 256-bin histogram used purely for display purposes on pages
    that don't otherwise need the full core algorithm's histogram output."""
    histogram = [0] * 256
    for row in image_list:
        for pixel in row:
            histogram[int(pixel)] += 1
    return histogram
