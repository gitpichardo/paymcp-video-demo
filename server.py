
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
    """Generates a short video and returns an MP4 file."""
    import tempfile
    import uuid
    from pathlib import Path
    
    # Generate the video
    data = await generate_video(prompt)
    
    # Save to a file in Downloads folder
    downloads_dir = Path.home() / "Downloads"
    filename = f"video_{uuid.uuid4().hex[:8]}.mp4"
    filepath = downloads_dir / filename
    
    filepath.write_bytes(data)
    
    return {
        "message": f"Video generated successfully!",
        "file_path": str(filepath),
        "file_size_mb": round(len(data) / (1024 * 1024), 2),
        "location": f"Saved to: {filepath}"
    }

if __name__ == "__main__":
    # Use stdio for Claude Desktop, streamable-http for other clients
    import sys
    if sys.stdin.isatty():
        # Running interactively, use HTTP
        mcp.run(transport="streamable-http")
    else:
        # Running from Claude Desktop or similar, use stdio
        mcp.run()
