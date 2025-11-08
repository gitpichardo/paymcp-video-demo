
import os
import asyncio
from lumaai import AsyncLumaAI

LUMA_API_KEY = os.getenv("LUMA_API_KEY")

async def generate_video(prompt: str) -> str:
    """
    Generate a video using Luma AI and return the download URL.
    
    Args:
        prompt: Text description of the video to generate
        
    Returns:
        str: URL to download the generated video (valid for 24 hours from Luma)
    """
    if not LUMA_API_KEY:
        raise RuntimeError("Missing LUMA_API_KEY")

    # Initialize Luma client
    client = AsyncLumaAI(auth_token=LUMA_API_KEY)

    # Create generation
    generation = await client.generations.create(
        prompt=prompt,
        model="ray-2"
    )

    # Poll for completion
    while generation.state not in ("completed", "failed"):
        await asyncio.sleep(3)
        generation = await client.generations.get(id=generation.id)
        print(f"Generation state: {generation.state}", file=__import__('sys').stderr)

    if generation.state == "failed":
        raise RuntimeError(f"Generation failed: {generation.failure_reason}")

    # Return the video URL (valid for 24 hours)
    return generation.assets.video
