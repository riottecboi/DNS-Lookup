import json
import os
from fastapi import APIRouter, HTTPException, Response, Request, Form, status, Depends
from fastapi.responses import RedirectResponse
from utils._dns import DomainLocator
from schemas._dnsRequest import DomainOrIP, ErrorResponse
from pydantic_core._pydantic_core import ValidationError
from cryptography.fernet import Fernet
from fastapi.templating import Jinja2Templates

key = Fernet.generate_key()
cipher_suite = Fernet(key)

folder = os.getcwd()
os.chdir("..")
path = os.getcwd()
templates = Jinja2Templates(directory=path+"/templates")

router = APIRouter()

def serialize_datetime(dt_or_list):
    if isinstance(dt_or_list, list):
        return [dt.isoformat() for dt in dt_or_list]
    if dt_or_list is None:
        return ''
    else:
        return dt_or_list.isoformat()

async def process_and_encrypt_data(domain_or_ip: str):
    try:
        validated_input = DomainOrIP(domain_or_ip=domain_or_ip)
        domain_or_ip = validated_input.domain_or_ip
        locator = DomainLocator(domain_or_ip)
        domain_info, domain_map = await locator.process_domain()
        if domain_info:
            domain_info['updated_date'] = serialize_datetime(domain_info['updated_date'])
            domain_info['creation_date'] = serialize_datetime(domain_info['creation_date'])
            domain_info['expiration_date'] = serialize_datetime(domain_info['expiration_date'])

            encrypted_domain_info = cipher_suite.encrypt(json.dumps(domain_info).encode()).decode()
            encrypted_domain_map = cipher_suite.encrypt(domain_map.encode()).decode()

            return encrypted_domain_info, encrypted_domain_map
        else:
            return None, None
    except ValidationError as e:
        raise HTTPException(status_code=400, detail={"error": "Not processing Domain/IP",
                                                     "message": "The input cannot process. Please try again."})

@router.post("/lookup", responses={400: {"model": ErrorResponse}})
async def dns_lookup(domain_or_ip: str = Form(...)):
    try:
        encrypted_domain_info, encrypted_domain_map = await process_and_encrypt_data(domain_or_ip)
        return RedirectResponse(url=f"/result?domain_info={encrypted_domain_info}&domain_map={encrypted_domain_map}", status_code=302)

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=ErrorResponse(error="Not processing Domain/IP",
                            message="The input cannot process. Please try again.").dict())

@router.get("/home")
async def get_template(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "domain_info": {}, "domain_map": {}})

@router.get("/result")
async def get_template(request: Request):
    domain_info = request.query_params.get('domain_info')
    domain_map = request.query_params.get('domain_map')

    if domain_info == 'None':
        domain_info = eval(domain_info)
        domain_map = eval(domain_map)

    else:
        decrypted_domain_info_json = cipher_suite.decrypt(domain_info.encode()).decode() if domain_info else None
        domain_info = json.loads(decrypted_domain_info_json)

        domain_map = cipher_suite.decrypt(domain_map.encode()).decode() if domain_map else None

    return templates.TemplateResponse("index.html", {"request": request, "domain_info": domain_info, "domain_map": domain_map})