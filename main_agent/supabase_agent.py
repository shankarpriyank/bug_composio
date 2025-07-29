from google.adk.agents import LlmAgent
from composio import Composio
from composio_google_adk import GoogleAdkProvider
from .request_context import get_current_tokens
import os
import logging

logger = logging.getLogger(__name__)
    tools = composio.tools.get(user_id=user_id, toolkits=["SUPABASE"])
    supabase_agent = LlmAgent(
        name="SUPABASE_AGENT",
        model="gemini-2.5-flash",
        tools=tools
    )
