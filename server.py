
import os
from pathlib import Path
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

# ---- Load video player component bundle
WEB_DIR = Path(__file__).parent / "web"
try:
    COMPONENT_JS = (WEB_DIR / "dist" / "video-player.js").read_text()
except FileNotFoundError:
    COMPONENT_JS = "console.error('Component bundle not found');"

# Register the video player UI component as an HTML resource
@mcp.resource("ui://widget/video-player.html")
def video_player_template() -> str:
    """HTML template for the video player component"""
    return {
        "uri": "ui://widget/video-player.html",
        "mimeType": "text/html+skybridge",
        "text": f'''
<div id="video-player-root"></div>
<script type="module">{COMPONENT_JS}</script>
        '''.strip(),
        "_meta": {
            "openai/widgetPrefersBorder": True,
            "openai/widgetDescription": "Displays an embedded video player with the generated AI video"
        }
    }

# ---- PayMCP mode selection
_mode_env = os.getenv("PAYMCP_MODE", "TWO_STEP").upper()
MODE = getattr(Mode, _mode_env, Mode.TWO_STEP)

PayMCP(
    mcp,
    providers={"walleot": {"apiKey": os.getenv("WALLEOT_API_KEY")}},
    mode=MODE
)

@mcp.tool(
    _meta={
        "openai/outputTemplate": "ui://widget/video-player.html",
        "openai/toolInvocation/invoking": "Generating video...",
        "openai/toolInvocation/invoked": "Video ready!"
    }
)
@price(PRICE_USD, "USD")
async def generate(prompt: str, ctx: Context):
    """Generates a short AI video and displays it with an embedded player."""
    # Generate the video and get the URL from Luma
    video_url = await generate_video(prompt)
    
    # Return structured content for the video player component
    return {
        "content": [
            {
                "type": "text",
                "text": f"✅ Generated video: {prompt}"
            }
        ],
        "structuredContent": {
            "video_url": video_url,
            "prompt": prompt
        }
    }

if __name__ == "__main__":
    # Run FastMCP server
    # Railway will map port 8000 to external URL even if bound to 127.0.0.1
    mcp.run(transport="streamable-http")
