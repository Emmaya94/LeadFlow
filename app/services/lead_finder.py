import os
import requests

SERP_API_KEY = os.getenv("SERP_API_KEY")


def find_leads(business_type, location, country, limit=5):
    if not SERP_API_KEY:
        raise ValueError("SERP_API_KEY is missing")

    query = f"{business_type} in {location} {country}"

    params = {
        "engine": "google_maps",
        "q": query,
        "api_key": SERP_API_KEY
    }

    try:
        response = requests.get(
            "https://serpapi.com/search",
            params=params,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

    except requests.RequestException as e:
        raise RuntimeError(f"SerpAPI request failed: {e}")

    leads = []

    for result in data.get("local_results", [])[:limit]:

        website = result.get("website")
        phone = result.get("phone")

        # 🎯 scoring simple
        if not website:
            score = "high"
            reason = "No website found, strong opportunity"
        elif website and not phone:
            score = "medium"
            reason = "Has website but limited contact info"
        else:
            score = "low"
            reason = "Has website and contact info"

        leads.append({
            "name": result.get("title"),
            "address": result.get("address"),
            "website": website,
            "phone": phone,
            "maps_link": result.get("link"),
            "score": score,
            "reason": reason
        })

    return leads
