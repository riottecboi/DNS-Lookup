import asyncio
import validators
import whois
import folium
from geopy import Nominatim
from schemas._whoisInfo import WhoisInfo

class DomainLocator:
    def __init__(self, domain: str):
        self.geolocator = Nominatim(user_agent="DNS_lookup")
        self.domain = domain
        self.domain_info = None
        self.return_info = None
        self.domain_map = None

    async def fetch_domain_info(self):
        try:
            loop = asyncio.get_event_loop()
            self.domain_info = await loop.run_in_executor(None, whois.whois, self.domain)
        except Exception as e:
            print(f"Error fetching WHOIS information for {self.domain}: {e}")

    async def get_coordinates(self, location):
        try:
            location = self.geolocator.geocode(location)
            if location:
                return location.latitude, location.longitude
            else:
                return None, None
        except Exception as e:
            print(f"Error fetching coordinates for {location}: {e}")
            return None, None

    async def plot_domain_location(self):
        if self.domain_info and self.domain_info.registrar:
            location = self.domain_info.address
            if self.domain_info.country and isinstance(self.domain_info.country, str):
                location = self.domain_info.country
            if self.domain_info.city and isinstance(self.domain_info.city, str):
                location = self.domain_info.city
            lat, lon = await self.get_coordinates(location)
            if lat and lon:
                map = folium.Map(location=[lat, lon], zoom_start=4)
                folium.Marker([lat, lon], popup=f"{self.domain}").add_to(map)
                self.domain_map = map.get_root()._repr_html_()
            else:
                print(f"Unable to find coordinates for location: {location}")
        else:
            print(f"No registrar information found for {self.domain}")

    async def map_whois_data(self, data):
        whois_fields = list(WhoisInfo.model_fields.keys())
        self.return_info = {}
        for field in whois_fields:
            if field in data:
                self.return_info[field] = data[field]
        return self.return_info

    async def process_domain(self):
        if self.domain:
            print(f"Processing domain: {self.domain}")
            await self.fetch_domain_info()
            await self.map_whois_data(self.domain_info)
            await self.plot_domain_location()
            return self.return_info, self.domain_map
        else:
            print("No valid domain to process")
            return None, None