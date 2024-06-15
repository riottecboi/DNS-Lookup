from fastapi import Request, APIRouter, Response
from fastapi.templating import Jinja2Templates
import os


router = APIRouter()

folder = os.getcwd()
os.chdir("..")
path = os.getcwd()

templates = Jinja2Templates(directory=path+"/templates")

@router.get("/home")
async def get_template(request: Request, response: Response):
    return templates.TemplateResponse("index.html", {"request": request, "domain_info": {}, "domain_map": {}})

@router.get("/result")
async def get_template(request: Request, response: Response):
    response_data = request.state.response_data
    return templates.TemplateResponse("index.html", {"request": request, "domain_info": {}, "domain_map": {}})