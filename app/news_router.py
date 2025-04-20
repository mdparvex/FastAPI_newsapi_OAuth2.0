from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi import Request
from app import database
from app.schemas import LatestNewsSchema, SaveLatestRequest
from app.models import LatestNewsModel
from app.utils import fetch_news
from app.models import LatestNewsModel

router = APIRouter()

@router.get("/")
async def get_all_news(
    request: Request,
    skip: int = 0,
    limit: int = 10,
    query: str = Query("news")
):
    
    if limit!=0:
        page = (skip // limit) + 1
    else:
        page = (skip//1)+1
    params = {"q": query, "page": page, "pageSize": limit}
    data = await fetch_news("everything", params)

    total = data.get("totalResults", 0)
    articles = data.get("articles", [])

    # Base URL
    base_url = str(request.url).split('?')[0]

    next_skip = skip + limit
    prev_skip = max(skip - limit, 0)

    next_url = f"{base_url}?skip={next_skip}&limit={limit}&query={query}" if next_skip < total else None
    prev_url = f"{base_url}?skip={prev_skip}&limit={limit}&query={query}" if skip > 0 else None

    return {
        "page": page,
        "pageSize": limit,
        "totalResults": total,
        "next": next_url,
        "previous": prev_url,
        "articles": articles
    }

@router.post("/save-latest")
async def save_latest_news(request: SaveLatestRequest, db: Session = Depends(database.get_db)):
    params = {}
    if request.country_code:
        params["country"] = request.country_code
    if not request.country_code:
        raise HTTPException(
            status_code=400,
            detail="countey_code must be provided"
        )

    data = await fetch_news("top-headlines", params)
    if request.source_id:
        filtered_articles = [
            article for article in data.get("articles", [])
            if article.get("source", {}).get("id") == request.source_id
        ]
        data["articles"] = filtered_articles
        data["totalResults"] = len(filtered_articles)
    else:
        data["totalResults"] = len(data.get("articles", []))

    save_count = 0
    try:
        for item in data["articles"]:
            exists = db.query(LatestNewsModel).filter_by(url=item["url"]).first()
            if exists:
                continue
            news = LatestNewsModel(
                title=item["title"],
                description=item["description"],
                url=item["url"],
                publishedAt=item["publishedAt"]
            )
            db.add(news)
            save_count +=1
            if save_count==3:
                break
        db.commit()
    except:
        raise HTTPException(status_code=400, detail="Database error")
    
    return {"message": f"Saved top {save_count} latest news"}

@router.get("/headlines/country/{country_code}")
async def get_headlines_by_country(country_code: str):
    return await fetch_news("top-headlines", {"country": country_code})

@router.get("/headlines/source/{source_id}")
async def get_headlines_by_source(source_id: str):
    return await fetch_news("top-headlines", {"sources": source_id})

@router.get("/headlines/filter")
async def get_headlines_filtered(
    country: str = Query(None),
    source: str = Query(None)
):
    
    if not country:
        raise HTTPException(
            status_code=400,
            detail="'country must be provided"
        )

    params = {}
    if country:
        params["country"] = country

    data = await fetch_news("top-headlines", params)

    if source:
        filtered_articles = [
            article for article in data.get("articles", [])
            if article.get("source", {}).get("id") == source
        ]
        data["articles"] = filtered_articles
        data["totalResults"] = len(filtered_articles)
    else:
        data["totalResults"] = len(data.get("articles", []))

    return data

