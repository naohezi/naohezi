import sys

sys.path.insert(1, 'modules')

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from system_monitor import show_drives, format_disk

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def storage_page(request: Request):
    return templates.TemplateResponse(
      "storage.html",
      {"request": request, "drives": show_drives()})

@app.post("/storage") 
async def format_disk_route( selected_disk: str = Form(...), filesystem: str = Form(...)):
    try:
      format_disk(selected_disk, filesystem)
      return RedirectResponse("/storage?message=Success", status_code=303)
    except Exception as e:
      return RedirectResponse(f"/storage?error={str(e)}", status_code=303)


