# app.py
from __future__ import annotations
import io
from pathlib import Path
import streamlit as st
from PIL import Image
from ascii_art.converter import image_to_ascii_string, CHAR_ASPECT  # reuse your core

st.set_page_config(page_title="Image → ASCII", page_icon="🖼️", layout="centered")
st.title("🖼️ → 🔠 Image to ASCII")
st.caption("Upload an image, tweak width / invert / charset, and download or copy the ASCII.")

uploaded = st.file_uploader("Upload an image (JPG/PNG/WebP)", type=["jpg","jpeg","png","webp"])

c1, c2 = st.columns(2)
with c1:
    width = st.slider("Output width (characters)", min_value=40, max_value=200, value=100, step=5)
with c2:
    invert = st.checkbox("Invert brightness", value=False)

preset = st.selectbox(
    "Character set (dark → light)",
    [
        "@%#*+=-:. ",                        # classic
        "@$B8&WM#*oahkbdpqwmZO0QLCJUYXz",    # dense
        "MWNQ#B$9@80Z7?+=~:,..  ",           # chunky
        "█▓▒░ .",                             # blocks
        "#A@%S?+;:,.",                        # short
    ],
    index=0
)

preview_height = st.slider("Preview height (px)", 200, 1200, 500, 50)

if uploaded:
    try:
        # Open directly from memory to avoid filesystem writes
        img_bytes = io.BytesIO(uploaded.getvalue())
        img = Image.open(img_bytes)  # converter will convert to grayscale

        # Use your existing pipeline via the fileless helper:
        # Save an in-memory path-free version by temporarily saving to bytes again:
        # But since image_to_ascii_string expects a path, let's add a tiny helper:
        # We can just run the same logic here for zero disk I/O:
        # --- begin inline conversion identical to converter.py ---
        img = img.convert("L")
        w, h = img.size
        new_h = max(1, int((h / w) * width * CHAR_ASPECT))
        img = img.resize((width, new_h))
        import numpy as np
        from ascii_art.converter import _map_pixels_to_chars  # uses your mapping
        arr = np.array(img, dtype=np.uint8)
        ascii_arr = _map_pixels_to_chars(arr, preset, invert)
        ascii_text = "\n".join("".join(row.tolist()) for row in ascii_arr)
        # --- end inline conversion ---

        st.subheader("Preview")
        # Show copyable code block (monospace + built-in copy button)
        st.code(ascii_text, language=None)

        # Also render a styled <pre> with adjustable height
        st.markdown(
            f"<div style='max-height:{preview_height}px; overflow:auto;'>"
            f"<pre style='margin:0; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;"
            f"font-size: 12px; line-height: 1.0; white-space: pre;'>{ascii_text}</pre></div>",
            unsafe_allow_html=True
        )

        st.download_button(
            "⬇️ Download ASCII as .txt",
            data=ascii_text.encode("utf-8"),
            file_name=Path(uploaded.name).stem + "_ascii.txt",
            mime="text/plain",
        )

    except Exception as e:
        st.error(f"Failed to convert: {e}")
