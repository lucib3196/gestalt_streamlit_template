from .core import init_session, get_settings
from .ui import (
    render_title,
    render_select_box,
    render_chatbot_description,
    render_chat,
    render_chat_input,
)
import streamlit as st

settings = get_settings()
init_session()


def render_ui():
    # Header Section
    render_title(settings.environment, thread_id=st.session_state.thread_id)
    render_select_box()
    render_chatbot_description()

    # Actual Chat Component
    render_chat()
    render_chat_input()
