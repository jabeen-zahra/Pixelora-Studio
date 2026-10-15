"""Sidebar brand bar + navigation menu.

Every item in the list -- whether it's a working page or a not-yet-built
placeholder -- is rendered as the same kind of button with the same icon
style, so the whole sidebar reads as one consistent list. Working pages are
clickable and switch the active page via st.session_state; placeholders are
rendered disabled.
"""

import streamlit as st
from ui.icons import ICONS


def _nav_item(page_key: str, material_icon: str, label: str, enabled: bool) -> None:
    is_active = enabled and st.session_state["active_page"] == page_key

    clicked = st.button(
        label,
        key=f"nav_{page_key}",
        icon=f":material/{material_icon}:",
        use_container_width=True,
        disabled=not enabled,
        type="primary" if is_active else "secondary",
    )

    if clicked and enabled and not is_active:
        st.session_state["active_page"] = page_key
        st.rerun()


def render_sidebar() -> str:
    """Renders the sidebar and returns the currently active page key."""
    if "active_page" not in st.session_state:
        st.session_state["active_page"] = "histogram_specification"

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
        _nav_item("histogram_specification", "bar_chart", "Histogram Specification", enabled=True)
        _nav_item("histogram_equalization", "equalizer", "Histogram Equalization", enabled=False)

        st.markdown('<div class="nav-section">Spatial Operations</div>', unsafe_allow_html=True)
        _nav_item("ace_filter", "contrast", "ACE Filter", enabled=True)
        _nav_item("convolution", "grid_on", "Convolution", enabled=False)
        _nav_item("segmentation", "category", "Segmentation", enabled=False)

        st.markdown('<div class="nav-section">Frequency Domain</div>', unsafe_allow_html=True)
        _nav_item("pseudocolor_frequency", "palette", "Pseudocolor (Frequency)", enabled=True)

    return st.session_state["active_page"]
