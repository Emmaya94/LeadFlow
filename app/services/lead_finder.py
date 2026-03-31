import requests
from app.core.settings import SERP_API_KEY


def find_leads(target_business_type: str, location: str, country: str, limit: int = 5):
    query = f"{target_business_type} in {location} {country}"

    params = {
        "engine": "google_maps",
        "q": query,
        "api_key": SERP_API_KEY,
    }

    response = requests.get("https://serpapi.com/search", params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    leads = []

    for result in data.get("local_results", [])[:limit]:
        leads.append(
            {
                "name": result.get("title", ""),
                "address": result.get("address"),
                "website": result.get("website"),
                "phone": result.get("phone"),
                "maps_link": result.get("link"),
            }
        )

    return leads
