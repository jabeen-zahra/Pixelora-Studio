import os

import streamlit as st

from ui.favicon import inject_favicon
from ui.sidebar import render_sidebar
from ui.pages import histogram_specification_page, ace_filter_page, pseudocolor_page

_HERE = os.path.dirname(os.path.abspath(__file__))
_ICON_PATH = os.path.join(_HERE, "assets", "pixelora_favicon.png")
_CSS_PATH = os.path.join(_HERE, "assets", "styles.css")

st.set_page_config(
    page_title="Pixelora Studio",
    page_icon=_ICON_PATH if os.path.exists(_ICON_PATH) else "🟧",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_favicon()

with open(_CSS_PATH, "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ================= SIDEBAR + ROUTING =================
active_page = render_sidebar()

PAGES = {
    "histogram_specification": histogram_specification_page,
    "ace_filter": ace_filter_page,
    "pseudocolor_frequency": pseudocolor_page,
}

PAGES[active_page].render()
