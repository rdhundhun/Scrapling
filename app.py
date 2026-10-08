from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scrapling.fetchers import DynamicFetcher

app = FastAPI(title="Scrapling Article Fetcher")


class ScrapeRequest(BaseModel):
    url: str


@app.get("/health")
async def health():
    return {"status": "ok", "service": "scrapling"}


@app.post("/scrape")
async def scrape(request: ScrapeRequest):
    try:
        page = DynamicFetcher.fetch(
            request.url,
            headless=True,
            network_idle=True,
            timeout=60000,
        )

        html = page.html_content

        return {
            "success": True,
            "url": request.url,
            "status": getattr(page, "status", None),
            "html": html,
            "htmlLength": len(html),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
