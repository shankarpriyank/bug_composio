import os
import uvicorn
import logging
import asyncio
from google.adk.cli.fast_api import get_fast_api_app
from google.adk.runners import Runner
from fastapi import Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from main_agent.request_context import RequestTokens, set_current_tokens, reset_tokens
from main_agent.agent import root_agent

from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get the directory where main.py is located
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Example session DB URL (e.g., SQLite)
SESSION_DB_URL = "sqlite:///./sessions.db"
# Example allowed origins for CORS
ALLOWED_ORIGINS = ["http://localhost", "http://localhost:8080", "*"]
# Set web=True if you intend to serve a web interface, False otherwise
SERVE_WEB_INTERFACE = True

# Initialize the FastAPI app at module level
app = get_fast_api_app(
    agents_dir=AGENT_DIR,
    session_service_uri=SESSION_DB_URL,
    allow_origins=ALLOWED_ORIGINS,
    web=SERVE_WEB_INTERFACE,
)


# Create a global variable for the runner
runner = None

@app.on_event("startup")
async def startup_event():
    global runner
    # Initialize the runner
    runner = Runner(app_name="loki_6", agent=root_agent)

@app.on_event("shutdown")
async def shutdown_event():
    global runner
    if runner:
        await runner.close()
        logger.info("Runner closed successfully")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
