import httpx
from fastapi import HTTPException
from app.config import NEWS_API_KEY, BASE_URL

async def fetch_news(endpoint: str, params: dict):
    headers = {"Authorization": f"Bearer {NEWS_API_KEY}"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/{endpoint}", params=params, headers=headers)
            response.raise_for_status()
            return response.json()
    except:
        raise HTTPException(status_code=401, detail="Something wrong with news API")