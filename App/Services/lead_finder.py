import requests

SERP_API_KEY = "TA_CLE_API_ICI"

def find_leads(business_type, location, country, limit=5):
    query = f"{business_type} in {location} {country}"

    params = {
        "engine": "google_maps",
        "q": query,
        "api_key": SERP_API_KEY
    }

    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()

    leads = []

    for result in data.get("local_results", [])[:limit]:
        leads.append({
            "name": result.get("title"),
            "address": result.get("address"),
            "website": result.get("website"),
            "phone": result.get("phone"),
            "maps_link": result.get("link")
        })

    return leads
