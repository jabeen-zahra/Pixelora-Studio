"""Assignment 1 -- Histogram Specification page."""

import numpy as np
import streamlit as st

from core.histogram_specification import histogram_specification
from ui.icons import icon
from ui.image_utils import load_image, image_bytes, fmt_bytes, mapping_table_html, show_histogram


def _render_upload_panel(label: str, hint: str, icon_name: str, key: str):
    """Renders one upload panel and returns the uploaded file (or None)."""
    with st.container(border=True):
        st.markdown(f"""
        <div class="panel-head">
            <div class="panel-title-row">{icon(icon_name)}<span class="panel-title">{label}</span></div>
            <div class="panel-hint">{hint}</div>
        </div>
        """, unsafe_allow_html=True)

        uploaded = st.file_uploader(
            f"Drop {label.lower()} here",
            type=["png", "jpg", "jpeg"],
            key=key,
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
                <div class="empty-title">No {label.lower()} loaded</div>
                <div class="empty-sub">Drag a photo here, or click to browse</div>
            </div>
            """, unsafe_allow_html=True)

        return uploaded


def render() -> None:
    st.markdown("""
    <div class="topbar">
        <div class="page-title">Histogram Specification</div>
        <div class="page-sub">Match the brightness and contrast of one image to another by using it as a reference.</div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2, gap="medium")

    with col_a:
        file_a = _render_upload_panel("Source Image", "Input A", "image", key="hs_source")

    with col_b:
        file_b = _render_upload_panel("Reference Image", "Input B", "target", key="hs_reference")

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    run_col, reset_col = st.columns([5, 1], gap="small")

    with run_col:
        run = st.button(
            "Apply Histogram Matching",
            type="primary",
            use_container_width=True,
            disabled=(file_a is None or file_b is None),
            key="hs_run"
        )

    with reset_col:
        if st.button("Reset", use_container_width=True, key="hs_reset"):
            st.session_state.pop("hs_result", None)
            st.session_state.pop("hs_output", None)
            st.rerun()

    if run:
        source = load_image(file_a)
        reference = load_image(file_b)

        with st.spinner("Computing cumulative distributions and mapping gray levels..."):
            result = histogram_specification(source.tolist(), reference.tolist())

        st.session_state["hs_result"] = result
        st.session_state["hs_output"] = np.array(result["output_image"], dtype=np.uint8)

    if "hs_result" in st.session_state:
        result = st.session_state["hs_result"]
        output = st.session_state["hs_output"]

        st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="topbar" style="margin-bottom:20px;">
            <div class="page-title" style="font-size:21px;">Results</div>
            <div class="page-sub">Output image, histogram comparison, and the full gray-level mapping table.</div>
        </div>
        """, unsafe_allow_html=True)

        t1, t2, t3 = st.tabs(["Output", "Histograms", "Mapping"])

        with t1:
            result_col, info_col = st.columns([3, 1], gap="medium")

            with result_col:
                with st.container(border=True):
                    st.markdown(f"""
                    <div class="panel-head">
                        <div class="panel-title-row">{icon('output')}<span class="panel-title">Matched Output</span></div>
                        <div class="panel-hint">Result</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown('<div class="img-wrap">', unsafe_allow_html=True)
                    st.image(output, use_container_width=True)
                    st.markdown(f"""
                    <div class="img-meta">
                        <span>{output.shape[1]} × {output.shape[0]} px</span>
                        <span>8-bit grayscale</span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
                    st.download_button(
                        "Export as PNG",
                        data=image_bytes(output),
                        file_name="pixelora_histogram_specification.png",
                        mime="image/png",
                        use_container_width=True,
                        key="hs_download"
                    )

            with info_col:
                with st.container(border=True):
                    st.markdown(f"""
                    <div class="panel-head">
                        <div class="panel-title-row">{icon('file')}<span class="panel-title">Image Info</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.metric("Width", f"{output.shape[1]} px")
                    st.metric("Height", f"{output.shape[0]} px")
                    st.metric("Bit depth", "8-bit")
                    st.metric("Gray levels", "256")
                    st.caption("Dimensions preserved from the source image.")

        with t2:
            h1, h2 = st.columns(2, gap="medium")

            with h1:
                with st.container(border=True):
                    st.markdown("""
                    <div class="plot-label">
                        <span class="plot-swatch" style="background:#8fa6d6"></span>
                        Source Histogram
                    </div>
                    """, unsafe_allow_html=True)
                    show_histogram(result["source_histogram"], "#8fa6d6")

                with st.container(border=True):
                    st.markdown("""
                    <div class="plot-label">
                        <span class="plot-swatch" style="background:#3dd68c"></span>
                        Output Histogram
                    </div>
                    """, unsafe_allow_html=True)
                    show_histogram(result["output_histogram"], "#3dd68c")

            with h2:
                with st.container(border=True):
                    st.markdown("""
                    <div class="plot-label">
                        <span class="plot-swatch" style="background:#ff8a3d"></span>
                        Reference Histogram
                    </div>
                    """, unsafe_allow_html=True)
                    show_histogram(result["reference_histogram"], "#ff8a3d")

                with st.container(border=True):
                    st.markdown(f"""
                    <div class="panel-head">
                        <div class="panel-title-row">{icon('info')}<span class="panel-title">Interpretation</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="note-box">
                        {icon('info')}
                        <p>The output distribution approximates the reference shape. Exact equality
                        isn't guaranteed, since gray levels are discrete and the mapping is many-to-one,
                        so some quantization error is expected.</p>
                    </div>
                    """, unsafe_allow_html=True)

        with t3:
            with st.container(border=True):
                st.markdown(f"""
                <div class="panel-head">
                    <div class="panel-title-row">{icon('swap')}<span class="panel-title">Gray-Level Mapping</span></div>
                    <div class="panel-hint">Source to Output</div>
                </div>
                """, unsafe_allow_html=True)

                mapping = result["mapping"]
                left, right = st.columns(2, gap="medium")

                with left:
                    st.caption("Levels 0 – 127")
                    st.markdown(mapping_table_html(range(128), mapping[:128]), unsafe_allow_html=True)

                with right:
                    st.caption("Levels 128 – 255")
                    st.markdown(mapping_table_html(range(128, 256), mapping[128:]), unsafe_allow_html=True)

    else:
        st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="big-empty">
            {icon('chart')}
            <h3>Ready when you are</h3>
            <p>Load a source and reference image above, then run <strong style="color:#ff8a3d">Apply Histogram Matching</strong>.</p>
        </div>
        """, unsafe_allow_html=True)
