from pydantic import BaseModel
from typing import List, Optional, Union

class WhoisInfo(BaseModel):
    domain_name: Optional[Union[str, List[str]]] = None
    registrar: Optional[str] = None
    whois_server: Optional[str] = None
    updated_date: Optional[Union[str, List[str]]] = None
    creation_date: Optional[Union[str, List[str]]] = None
    expiration_date: Optional[Union[str, List[str]]] = None
    name_servers: Optional[Union[str, List[str]]] = None
    emails: Optional[Union[str, List[str]]] = None
    org: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None