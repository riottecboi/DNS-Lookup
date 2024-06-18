from fastapi import FastAPI
from routes import _dnsLookup
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(
    title="DNS Lookup API",
    description="API for getting whois information and location of domain or IP",
    version="1.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
    contact={
        "name": "Tran Vinh Liem",
        "email": "riottecboi@gmail.com",
        "url": "https://about.riotteboi.com"
    }
)
folder = os.getcwd()

app.mount("/static", StaticFiles(directory=folder+"/static", html=True), name="static")
app.include_router(_dnsLookup.router)