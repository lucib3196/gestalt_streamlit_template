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


def index_sources(sources: List[SourceRef]):
    index = {}
    for src in sources:
        key = (src.lecture_title, Path(src.source_pdf))
        index.setdefault(key, src)  # keep first occurrence
    return index


def toggle_source(key: str):
    if st.session_state.get("active_source") == key:
        st.session_state["active_source"] = None
    else:
        st.session_state["active_source"] = key


def show_sources():
    sources: List[SourceRef] = st.session_state.get("sources", [])
    indexed_sources = index_sources(sources)
    if indexed_sources:
        st.markdown("### Sources")

        for index in indexed_sources:

            is_active = st.session_state.get("active_source") == index
            label = f"▼ {index[0]}" if is_active else f"▶ {index[0]}"
            st.button(
                label,
                key=f"btn_{index[0]}",
                on_click=toggle_source,
                args=(index,),
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
    source_index = index_sources(sources)
    active_key = st.session_state.get("active_source")
    active_source = source_index.get(active_key, None)
    if active_source:
        pdf_path = (
            Path("gestalt_streamlit_template") / active_source.source_pdf
        ).resolve()
        rotated_bytes = rotate_pdf(pdf_path, st.session_state["source_rotation"])
        st.pdf(rotated_bytes)


def source_view():
    show_sources()
    render_selected_source()
    rotation_buttons()
