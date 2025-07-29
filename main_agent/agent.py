from google.adk.agents import LlmAgent, BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams, StdioServerParameters
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.planners import BuiltInPlanner
from google.adk.tools import BaseTool, ToolContext, agent_tool
from typing import List, Optional, Dict, Any
from google.genai import types
from .request_context import get_current_tokens
from .search_agent import search_agent
from google.adk.models.anthropic_llm import Claude
from google.adk.models.registry import LLMRegistry
import nest_asyncio
import logging
from composio import Composio
from composio_google_adk import GoogleAdkProvider

from .supabase_agent import supabase_agent

from dotenv import load_dotenv
load_dotenv(".env")

# Configure logging for this module
logger = logging.getLogger(__name__)

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()






# Create the search agent tool wrapper
search_tool = agent_tool.AgentTool(agent=supabase_agent)
# Note: ScrapeElementFromWebsiteTool removed due to compatibility issues with Python 3.13
# scrape_tool = ScrapeElementFromWebsiteTool()



# Initialize the root agent with callbacks
root_agent = LlmAgent(
    name="Loki",
    model="gemini-2.5-flash",
    tools=[search_tool],
)