import json
from fastapi import APIRouter, HTTPException, Response, Request, Form, status
from fastapi.responses import RedirectResponse
from utils._dns import DomainLocator
from schemas._dnsRequest import DomainOrIP, ErrorResponse
from pydantic_core._pydantic_core import ValidationError

router = APIRouter()

@router.post("/lookup", tags=["Whois"], responses={400: {"model": ErrorResponse}})
async def dns_lookup(request: Request, domain_or_ip: str = Form(...)):
    try:
        validated_input = DomainOrIP(domain_or_ip=domain_or_ip)
        domain_or_ip = validated_input.domain_or_ip
        locator = DomainLocator(domain_or_ip)
        domain_info, domain_map = await locator.process_domain()
        return RedirectResponse(url="/result", status_code=status.HTTP_302_FOUND)


    except ValidationError as e:
        raise HTTPException(status_code=400, detail=ErrorResponse(error="Not processing Domain/IP",
                            message="The input cannot process. Please try again.").dict())