from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Youtube Downloader", description="Downloads youtube videos given the url link")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})