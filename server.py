
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

# Create ASGI app for uvicorn (Railway deployment)
# This allows uvicorn to run the app with explicit host binding
app = mcp.http_app()

if __name__ == "__main__":
    # Always run in HTTP mode (streamable-http transport)
    # For Railway: use start.sh which runs uvicorn with host=0.0.0.0
    mcp.run(transport="streamable-http")
