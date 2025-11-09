
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
    """Generates a short video and returns a download URL with embedded preview."""
    # Generate the video and get the URL from Luma
    video_url = await generate_video(prompt)
    
    # Return formatted markdown that ChatGPT can render with video embed
    return f"""✅ **Video generated successfully!**

**Prompt:** {prompt}

**Watch your video:**

{video_url}

🎥 **Direct download:** [Click here to download]({video_url})

💡 **Note:** Video link is valid for 24 hours from Luma AI.
"""

if __name__ == "__main__":
    # Run FastMCP server
    # Railway will map port 8000 to external URL even if bound to 127.0.0.1
    mcp.run(transport="streamable-http")
