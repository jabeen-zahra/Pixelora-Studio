"""Assignment 2, Part 1 -- Adaptive Contrast Enhancement (ACE) Filter page."""

import numpy as np
import streamlit as st

from core.ace_filter import ace_filter
from ui.icons import icon
from ui.image_utils import load_image, image_bytes, fmt_bytes, show_histogram, calculate_histogram_for_display


def render() -> None:
    st.markdown("""
    <div class="topbar">
        <div class="page-title">Adaptive Contrast Enhancement (ACE) Filter</div>
        <div class="page-sub">Boost contrast separately in each part of the image, based on how bright and detailed that specific area already is, instead of applying one flat adjustment everywhere.</div>
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
                key="ace_source",
                label_visibility="collapsed"
            )

            if uploaded:
                img = load_image(uploaded)
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
                    <span>8-bit grayscale</span>
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
                <div class="panel-title-row">{icon('sliders')}<span class="panel-title">Filter Parameters</span></div>
            </div>
            """, unsafe_allow_html=True)

            window_size = st.select_slider(
                "Window size (n × n)",
                options=[3, 5, 7, 9, 11, 15, 21],
                value=5,
                key="ace_window"
            )
            k1 = st.slider("k1 (contrast strength)", 0.0, 1.0, 0.5, 0.05, key="ace_k1")
            k2 = st.slider("k2 (brightness retention)", 0.0, 1.0, 0.5, 0.05, key="ace_k2")
            apply_stretch = st.checkbox(
                "Apply histogram stretch afterward",
                value=True,
                key="ace_stretch",
                help="Often makes the result easier to see clearly."
            )

            st.caption(
                "A larger window looks at a bigger neighborhood around each "
                "pixel, giving a smoother, less noisy result. A thin strip "
                "around the edge of the image is left unchanged."
            )

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    run_col, reset_col = st.columns([5, 1], gap="small")

    with run_col:
        run = st.button(
            "Apply ACE Filter",
            type="primary",
            use_container_width=True,
            disabled=(uploaded is None),
            key="ace_run"
        )

    with reset_col:
        if st.button("Reset", use_container_width=True, key="ace_reset"):
            st.session_state.pop("ace_result", None)
            st.session_state.pop("ace_output", None)
            st.rerun()

    if run:
        source = load_image(uploaded)

        with st.spinner("Sliding the window across the image and computing local statistics..."):
            result = ace_filter(
                source.tolist(),
                window_size=window_size,
                k1=k1,
                k2=k2,
                apply_stretch=apply_stretch
            )

        st.session_state["ace_result"] = result
        st.session_state["ace_output"] = np.array(result["output_image"], dtype=np.uint8)
        st.session_state["ace_original"] = source

    if "ace_result" in st.session_state:
        result = st.session_state["ace_result"]
        output = st.session_state["ace_output"]
        original = st.session_state["ace_original"]

        st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="topbar" style="margin-bottom:20px;">
            <div class="page-title" style="font-size:21px;">Results</div>
            <div class="page-sub">Used a {result['window_size']}×{result['window_size']} window with k1 = {result['k1']} and k2 = {result['k2']}.{' A histogram stretch was applied afterward for better visibility.' if result['stretch_applied'] else ''}</div>
        </div>
        """, unsafe_allow_html=True)

        t1, t2 = st.tabs(["Output", "Histograms"])

        with t1:
            before_col, after_col = st.columns(2, gap="medium")

            with before_col:
                with st.container(border=True):
                    st.markdown(f"""
                    <div class="panel-head">
                        <div class="panel-title-row">{icon('image')}<span class="panel-title">Original</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown('<div class="img-wrap">', unsafe_allow_html=True)
                    st.image(original, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

            with after_col:
                with st.container(border=True):
                    st.markdown(f"""
                    <div class="panel-head">
                        <div class="panel-title-row">{icon('output')}<span class="panel-title">ACE Enhanced</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown('<div class="img-wrap">', unsafe_allow_html=True)
                    st.image(output, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
                    st.download_button(
                        "Export as PNG",
                        data=image_bytes(output),
                        file_name="pixelora_ace_filter.png",
                        mime="image/png",
                        use_container_width=True,
                        key="ace_download"
                    )

        with t2:
            h1, h2 = st.columns(2, gap="medium")

            with h1:
                with st.container(border=True):
                    st.markdown("""
                    <div class="plot-label">
                        <span class="plot-swatch" style="background:#8fa6d6"></span>
                        Original Histogram
                    </div>
                    """, unsafe_allow_html=True)
                    show_histogram(calculate_histogram_for_display(original.tolist()), "#8fa6d6")

            with h2:
                with st.container(border=True):
                    st.markdown("""
                    <div class="plot-label">
                        <span class="plot-swatch" style="background:#3dd68c"></span>
                        Enhanced Histogram
                    </div>
                    """, unsafe_allow_html=True)
                    show_histogram(calculate_histogram_for_display(output.tolist()), "#3dd68c")

    else:
        st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="big-empty">
            {icon('sliders')}
            <h3>Ready when you are</h3>
            <p>Load an image, set your window size and gain/mean constants, then run <strong style="color:#ff8a3d">Apply ACE Filter</strong>.</p>
        </div>
        """, unsafe_allow_html=True)
