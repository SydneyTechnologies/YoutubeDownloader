from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import yt_dlp as youtube_dl
import schema
import utils


# CONSTANTS 
TITLE = "Youtube Downloader"
DESCRIPTION = "Downloads youtube videos given the url link"


# SETTING UP FASTAPI APPLICATION, STATIC FILES, AND TEMPLATES
app = FastAPI(title=TITLE, description=DESCRIPTION)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# SETTING UP ROUTES 
@app.get("/")
def index(request: Request):
    # this route hosts a html template for the application
    template_name = "index.html"
    context = {"request": request}
    return templates.TemplateResponse(name=template_name, context=context)


@app.post("/download/")
def download(request_info: schema.YtVideoRequestInfo, quality : str = Depends(lambda q: utils.resolveQuality(q))):
      # takes in the request body type of videoOptions containing the link and the 
      # video and audio quality to be downloaded
      target_url = request_info.url
      print(f"Youtube video link: {target_url}")
      print(f"download quality: {quality}")
      print(f"download format: {request_info.format}")

                
      ydlOpts ={
        'format': quality,
        'postprocessors': [  # Post-processing options
        {'key': 'FFmpegExtractAudio'},  # Extract audio
        {'key': 'FFmpegVideoConvertor', 'preferedformat': request_info.format },  # Convert video to requested format
        ],
      }

      if target_url: 
        with youtube_dl.YoutubeDL(ydlOpts) as ydl:
            ydl.download([target_url])
            return ""
      return HTTPException(status.HTTP_400_BAD_REQUEST, "Youtube URL link missing")