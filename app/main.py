from fastapi import FastAPI
from routes import _dnsLookup, _home
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(
    title="DNS Lookup API",
    description="API for getting whois information and location of domain or IP",
    version="1.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    openapi_tags=[
        {
            "name": "Whois",
            "description": "The Whois information from the input of domain or ip"
        }
    ],
    contact={
        "name": "Tran Vinh Liem",
        "email": "riottecboi@gmail.com",
        "url": "https://about.riotteboi.com"
    }
)
folder = os.getcwd()
os.chdir("..")
path = os.getcwd()

app.mount("/static", StaticFiles(directory=folder+"/static", html=True), name="static")

app.include_router(_dnsLookup.router, prefix="/api")
app.include_router(_home.router)
