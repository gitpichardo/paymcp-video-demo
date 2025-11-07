
import os, aiohttp, asyncio

LUMA_API_KEY = os.getenv("LUMA_API_KEY")
BASE = "https://api.lumalabs.ai/dream-machine/v1"

async def generate_video(prompt: str) -> bytes:
    if not LUMA_API_KEY:
        raise RuntimeError("Missing LUMA_API_KEY")

    headers = {
        "Authorization": f"Bearer {LUMA_API_KEY}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        # Submit job
        async with session.post(f"{BASE}/videos", json={"prompt": prompt}, headers=headers) as r:
            r.raise_for_status()
            job = await r.json()
        job_id = job["id"]

        # Poll status
        status = None
        while status not in ("completed", "failed"):
            await asyncio.sleep(2)
            async with session.get(f"{BASE}/videos/{job_id}", headers=headers) as r:
                r.raise_for_status()
                job = await r.json()
                status = job.get("status")

        if status == "failed":
            raise RuntimeError(job.get("error", "Video generation failed"))

        # Download mp4
        video_url = job["result"]["video"]["url"]
        async with session.get(video_url, headers=headers) as r:
            r.raise_for_status()
            return await r.read()
