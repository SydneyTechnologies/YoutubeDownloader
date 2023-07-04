from fastapi import FastAPI, Request, Body
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl
import yt_dlp as youtube_dl
import ssl
import utils

# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

app = FastAPI(title="Youtube Downloader", description="Downloads youtube videos given the url link")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class videoOptions(BaseModel):
    url: HttpUrl
    quality: utils.FormatCategory

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})


@app.post("/download/")
def download(videoOption: videoOptions):
      baseUrl = "https://www.youtube.com/watch?v="
      videoId = videoOption.url.split("=")[1]
      targetUrl = baseUrl+videoId
      ydlOpts ={
          'format': videoOption.quality.value,
              'postprocessors': [  # Post-processing options
        {'key': 'FFmpegExtractAudio'},  # Extract audio
        {'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'},  # Convert video to MP4
    ],
      }
      with youtube_dl.YoutubeDL(ydlOpts) as ydl:
        ydl.download([targetUrl])
        return ""