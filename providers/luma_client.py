
import os
import asyncio
import aiohttp
from lumaai import AsyncLumaAI

LUMA_API_KEY = os.getenv("LUMA_API_KEY")

async def generate_video(prompt: str) -> bytes:
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

    # Download the video
    video_url = generation.assets.video
    async with aiohttp.ClientSession() as session:
        async with session.get(video_url) as response:
            response.raise_for_status()
            return await response.read()
