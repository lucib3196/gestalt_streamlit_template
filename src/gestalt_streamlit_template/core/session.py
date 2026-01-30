from typing import Any, List
from pydantic import BaseModel
import streamlit as st
from .config import CHAT_NAMES
from services.llm_services import initialize_thread_id
from models import SourceRef

show_sources = st.secrets.get("SHOW_SOURCES",False)

class DefaultState(BaseModel):
    messages: List[Any] = []
    thread_id: str | None = None
    chat_select: CHAT_NAMES | None
    sources: List[SourceRef] = []
    active_source: str = ""
    source_rotation: int = 0
    show_sources: bool = show_sources


DEFAULT_STATE = DefaultState(
    messages=[], chat_select=None, thread_id=initialize_thread_id()
)


def init_session():
    for key, value in DEFAULT_STATE.model_dump().items():
        if key not in st.session_state:
            st.session_state[key] = value
            
