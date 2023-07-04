from pydantic import BaseModel, HttpUrl

class YtVideoRequestInfo(BaseModel):
    url: HttpUrl
    quality: str | None = "best"
    format: str | None = "mp4"