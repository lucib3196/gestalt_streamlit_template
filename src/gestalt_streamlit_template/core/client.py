from langgraph_sdk import get_client
from .app_settings import get_settings

settings = get_settings()
client = get_client(url=settings.url, api_key=settings.langsmith_api_key)
