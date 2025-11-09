
import os
from mcp.server.fastmcp import FastMCP, Context
from fastmcp.utilities.types import File
from paymcp import PayMCP, Mode, price

# Optional: load .env for local dev
if os.getenv("ENV", "development") == "development":
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except Exception:
        pass

# ---- Provider selection
VIDEO_PROVIDER = os.getenv("VIDEO_PROVIDER", "luma").lower()
PRICE_USD = float(os.getenv("PRICE_USD", "0.60"))

if VIDEO_PROVIDER == "luma":
    from providers.luma_client import generate_video
else:
    raise RuntimeError(f"Unsupported VIDEO_PROVIDER: {VIDEO_PROVIDER}")

# ---- MCP server
mcp = FastMCP("Video generator")

# ---- PayMCP mode selection
_mode_env = os.getenv("PAYMCP_MODE", "TWO_STEP").upper()
MODE = getattr(Mode, _mode_env, Mode.TWO_STEP)

PayMCP(
    mcp,
    providers={"walleot": {"apiKey": os.getenv("WALLEOT_API_KEY")}},
    mode=MODE
)

@mcp.tool()
@price(PRICE_USD, "USD")
async def generate(prompt: str, ctx: Context):
    """Generates a short video and returns a download URL."""
    # Generate the video and get the URL from Luma
    video_url = await generate_video(prompt)
    
    return {
        "message": "Video generated successfully!",
        "video_url": video_url,
        "prompt": prompt,
        "instructions": "Click the video_url to download or view your generated video"
    }

# Export the ASGI app for uvicorn
# This allows us to run: uvicorn server:asgi_app --host 0.0.0.0 --port 8000
def create_app():
    """Create and return the ASGI application."""
    from fastmcp.server.http.streamable_http_manager import StreamableHTTPManager
    from mcp.server.fastmcp.server import _make_request_handlers
    
    # Get request handlers from FastMCP
    handlers = _make_request_handlers(mcp._mcp)
    
    # Create the streamable HTTP manager
    manager = StreamableHTTPManager(handlers)
    
    # Return the ASGI app
    return manager.create_asgi_app()

# Create the app at module level so uvicorn can find it
asgi_app = create_app()

if __name__ == "__main__":
    # For local development only
    import uvicorn
    import os
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(asgi_app, host="0.0.0.0", port=port)
