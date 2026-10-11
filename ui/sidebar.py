"""Sidebar brand bar + navigation menu."""

import streamlit as st
from ui.icons import ICONS, icon


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown(f"""
        <div class="brand-bar">
            <div class="logo-mark">{ICONS['logo']}</div>
            <div class="brand-text">
                <div class="brand-name">Pixelora Studio</div>
                <div class="brand-sub">Imaging Toolkit</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="nav-section">Point Operations</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="nav-item active">{icon("histogram")}Histogram Specification</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="nav-item disabled">{icon("equalize")}Histogram Equalization</div>',
            unsafe_allow_html=True
        )

        st.markdown('<div class="nav-section">Spatial Operations</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="nav-item disabled">{icon("filter")}Image Filtering</div>'
            f'<div class="nav-item disabled">{icon("grid")}Convolution</div>'
            f'<div class="nav-item disabled">{icon("segment")}Segmentation</div>',
            unsafe_allow_html=True
        )
