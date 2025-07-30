import requests
from .models import EdgeGroup

BASE_URL = "https://api.conceptnet.io"

class ConceptNetAPI:
    def __init__(self, language="en"):
        self.language = language

    def _normalize(self, term):
        return term.strip().lower().replace(" ", "_")

    def lookup(self, term, limit=10, offset=0):
        term = self._normalize(term)
        url = f"{BASE_URL}/c/{self.language}/{term}?limit={limit}&offset={offset}"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code} - {response.text}")
        data = response.json()
        return EdgeGroup(data.get("edges", []))
