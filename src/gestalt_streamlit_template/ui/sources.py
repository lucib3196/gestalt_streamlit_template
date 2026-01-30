from pathlib import Path
import fitz
from io import BytesIO
import streamlit as st
from models import SourceRef
from typing import List


def rotate_pdf(pdf_path: Path | str, rotation: int) -> bytes:
    doc = fitz.open(pdf_path)
    for page in doc:
        page.set_rotation(rotation)
    buffer = BytesIO()
    doc.save(buffer)
    doc.close()
    return buffer.getvalue()


def toggle_source(key: str):
    if st.session_state.get("active_source") == key:
        st.session_state["active_source"] = None
    else:
        st.session_state["active_source"] = key


def show_sources():
    sources: List[SourceRef] = st.session_state.get("sources", [])
    if sources:
        st.markdown("### Sources")

        for src in sources:
            source_key = (src.source_id, src.page)
            is_active = st.session_state.get("active_source") == source_key
            label = (
                f"▼ {src.title} (p. {src.page})"
                if is_active
                else f"▶ {src.title} (p. {src.page})"
            )
            st.button(
                label,
                key=f"btn_{src.source_id}_{src.page}",
                on_click=toggle_source,
                args=(source_key,),
            )


def rotation_buttons():
    if not st.session_state.get("active_source"):
        return
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⟲ Rotate"):
            st.session_state["source_rotation"] -= 90

    with col2:
        if st.button("⟳ Rotate"):
            st.session_state["source_rotation"] += 90


def render_selected_source():
    sources: List[SourceRef] = st.session_state.get("sources", [])
    active_key = st.session_state.get("active_source")
    if active_key:
        active_src = next(
            src for src in sources if (src.source_id, src.page) == active_key
        )
        pdf_path = (Path("gestalt_streamlit_template") / active_src.path).resolve()
        rotated_bytes = rotate_pdf(pdf_path, st.session_state["source_rotation"])
        st.pdf(rotated_bytes)


def source_view():
    show_sources()
    render_selected_source()
    rotation_buttons()
