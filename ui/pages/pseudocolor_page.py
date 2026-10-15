"""Assignment 2, Part 2 -- Pseudocolor in the Frequency Domain page."""

import numpy as np
import streamlit as st

from core.pseudocolor_frequency import pseudocolor_frequency_domain
from ui.icons import icon
from ui.image_utils import load_image, image_bytes, fmt_bytes

BAND_LABELS = {
    "lowpass": "Lowpass",
    "bandpass": "Bandpass",
    "highpass": "Highpass",
}
BAND_KEYS = list(BAND_LABELS.keys())


def render() -> None:
    st.markdown("""
    <div class="topbar">
        <div class="page-title">Pseudocolor (Frequency Domain)</div>
        <div class="page-sub">Turn a grayscale image into a false-color image by highlighting its coarse, medium, and fine details in different colors.</div>
    </div>
    """, unsafe_allow_html=True)

    upload_col, controls_col = st.columns([3, 2], gap="medium")

    with upload_col:
        with st.container(border=True):
            st.markdown(f"""
            <div class="panel-head">
                <div class="panel-title-row">{icon('image')}<span class="panel-title">Input Image</span></div>
                <div class="panel-hint">Source</div>
            </div>
            """, unsafe_allow_html=True)

            uploaded = st.file_uploader(
                "Drop an image here",
                type=["png", "jpg", "jpeg"],
                key="pc_source",
                label_visibility="collapsed"
            )

            max_freq = 128
            if uploaded:
                img = load_image(uploaded)
                max_freq = max(1, min(img.shape[0], img.shape[1]) // 2)

                st.markdown(f"""
                <div class="file-chip">
                    <div class="top-row">
                        {icon('image')}
                        <span class="name">{uploaded.name}</span>
                    </div>
                    <span class="size">{fmt_bytes(uploaded.size)}</span>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('<div class="img-wrap">', unsafe_allow_html=True)
                st.image(img, use_container_width=True)
                st.markdown(f"""
                <div class="img-meta">
                    <span>{img.shape[1]} × {img.shape[0]} px</span>
                    <span>highest frequency ≈ {max_freq}</span>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="empty-state">
                    {icon('upload')}
                    <div class="empty-title">No image loaded</div>
                    <div class="empty-sub">Drag a photo here, or click to browse</div>
                </div>
                """, unsafe_allow_html=True)

    with controls_col:
        with st.container(border=True):
            st.markdown(f"""
            <div class="panel-head">
                <div class="panel-title-row">{icon('waves')}<span class="panel-title">Cutoff Frequencies</span></div>
            </div>
            """, unsafe_allow_html=True)

            cutoff_low = st.slider("Lowpass / Bandpass cutoff (f₁)", 1, max_freq, min(10, max_freq), key="pc_f1")
            cutoff_high = st.slider("Bandpass / Highpass cutoff (f₂)", 1, max_freq, min(max(cutoff_low + 1, 20), max_freq), key="pc_f2")

            if cutoff_high <= cutoff_low:
                st.markdown("""
                <div class="warn-box">
                    <p>The second cutoff needs to be higher than the first, so the three bands don't overlap. Please adjust the sliders.</p>
                </div>
                """, unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown(f"""
            <div class="panel-head">
                <div class="panel-title-row">{icon('palette')}<span class="panel-title">Channel Assignment</span></div>
            </div>
            """, unsafe_allow_html=True)

            r_band = st.selectbox("Red channel shows", BAND_KEYS, format_func=lambda k: BAND_LABELS[k], index=0, key="pc_r")
            g_band = st.selectbox("Green channel shows", BAND_KEYS, format_func=lambda k: BAND_LABELS[k], index=1, key="pc_g")
            b_band = st.selectbox("Blue channel shows", BAND_KEYS, format_func=lambda k: BAND_LABELS[k], index=2, key="pc_b")

            assignment = {"R": r_band, "G": g_band, "B": b_band}
            valid_assignment = len(set(assignment.values())) == 3

            if not valid_assignment:
                st.markdown("""
                <div class="warn-box">
                    <p>Each band (Lowpass, Bandpass, Highpass) must go to a different channel.</p>
                </div>
                """, unsafe_allow_html=True)

            equalize = st.checkbox(
                "Apply histogram equalization to each band",
                value=False,
                key="pc_equalize",
                help="Can make the color differences more visible. Whether it helps depends on the image."
            )

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    run_col, reset_col = st.columns([5, 1], gap="small")

    can_run = (
        uploaded is not None
        and cutoff_high > cutoff_low
        and valid_assignment
    )

    with run_col:
        run = st.button(
            "Apply Pseudocolor Mapping",
            type="primary",
            use_container_width=True,
            disabled=not can_run,
            key="pc_run"
        )

    with reset_col:
        if st.button("Reset", use_container_width=True, key="pc_reset"):
            st.session_state.pop("pc_result", None)
            st.rerun()

    if run:
        source = load_image(uploaded)

        with st.spinner("Computing the Fourier transform and filtering each frequency band..."):
            result = pseudocolor_frequency_domain(
                source.tolist(),
                cutoff_low=cutoff_low,
                cutoff_high=cutoff_high,
                channel_assignment=assignment,
                equalize=equalize
            )

        st.session_state["pc_result"] = result
        st.session_state["pc_original"] = source

    if "pc_result" in st.session_state:
        result = st.session_state["pc_result"]
        original = st.session_state["pc_original"]

        st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="topbar" style="margin-bottom:20px;">
            <div class="page-title" style="font-size:21px;">Results</div>
            <div class="page-sub">Cutoff frequencies: {result['cutoff_low']} and {result['cutoff_high']}. Red is {BAND_LABELS[result['channel_assignment']['R']]}, Green is {BAND_LABELS[result['channel_assignment']['G']]}, Blue is {BAND_LABELS[result['channel_assignment']['B']]}.{' Histogram equalization was applied to each band.' if result['equalize_applied'] else ''}</div>
        </div>
        """, unsafe_allow_html=True)

        t1, t2 = st.tabs(["Pseudocolor Output", "Individual Bands"])

        with t1:
            before_col, after_col = st.columns(2, gap="medium")

            with before_col:
                with st.container(border=True):
                    st.markdown(f"""
                    <div class="panel-head">
                        <div class="panel-title-row">{icon('image')}<span class="panel-title">Original (Grayscale)</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown('<div class="img-wrap">', unsafe_allow_html=True)
                    st.image(original, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

            with after_col:
                with st.container(border=True):
                    st.markdown(f"""
                    <div class="panel-head">
                        <div class="panel-title-row">{icon('palette')}<span class="panel-title">Pseudocolor Result</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown('<div class="img-wrap">', unsafe_allow_html=True)
                    st.image(result["rgb_image"], use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
                    st.download_button(
                        "Export as PNG",
                        data=image_bytes(result["rgb_image"]),
                        file_name="pixelora_pseudocolor.png",
                        mime="image/png",
                        use_container_width=True,
                        key="pc_download"
                    )

        with t2:
            b1, b2, b3 = st.columns(3, gap="medium")

            band_previews = [
                (b1, "lowpass", "#8fa6d6"),
                (b2, "bandpass", "#3dd68c"),
                (b3, "highpass", "#ff8a3d"),
            ]

            for column, band_key, swatch_color in band_previews:
                with column:
                    with st.container(border=True):
                        st.markdown(f"""
                        <div class="plot-label">
                            <span class="plot-swatch" style="background:{swatch_color}"></span>
                            {BAND_LABELS[band_key]}
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown('<div class="img-wrap">', unsafe_allow_html=True)
                        st.image(result[f"{band_key}_image"], use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="big-empty">
            {icon('waves')}
            <h3>Ready when you are</h3>
            <p>Load an image, set your cutoff frequencies and channel assignment, then run <strong style="color:#ff8a3d">Apply Pseudocolor Mapping</strong>.</p>
        </div>
        """, unsafe_allow_html=True)
