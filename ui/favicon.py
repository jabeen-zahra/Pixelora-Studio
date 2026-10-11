"""Injects the Pixelora Studio logo mark as the browser tab favicon.

Streamlit's st.markdown(unsafe_allow_html=True) does NOT execute <script> tags --
it only inserts them as inert HTML. components.html() renders inside an iframe
and actually runs the script, so we reach into window.parent.document to swap
the favicon on the real page.
"""

import base64
import streamlit.components.v1 as components

_FAVICON_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ff8a3d"/>
      <stop offset="100%" stop-color="#e05500"/>
    </linearGradient>
  </defs>
  <rect width="64" height="64" rx="15" fill="url(#g)"/>
  <g transform="translate(13,13) scale(1.65)">
    <path d="M4 4h10a5 5 0 0 1 0 10H8v6H4V4Zm4 3.6v6.8h6a3.4 3.4 0 0 0 0-6.8H8Z" fill="#ffffff"/>
  </g>
</svg>
""".strip()


def inject_favicon() -> None:
    """Replace the browser tab favicon with the Pixelora Studio logo mark."""
    favicon_b64 = base64.b64encode(_FAVICON_SVG.encode()).decode()

    components.html(f"""
    <script>
    (function() {{
        var doc = window.parent.document;
        var existing = doc.querySelectorAll("link[rel~='icon']");
        existing.forEach(function(el) {{ el.remove(); }});
        var link = doc.createElement('link');
        link.rel = 'icon';
        link.type = 'image/svg+xml';
        link.href = "data:image/svg+xml;base64,{favicon_b64}";
        doc.head.appendChild(link);
    }})();
    </script>
    """, height=0, width=0)
