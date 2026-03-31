import os

SERP_API_KEY = os.getenv("SERP_API_KEY")


def find_leads(business_type, location, country, limit=5):

    # 🔥 Si pas de clé → simulation
    if not SERP_API_KEY:
        return [
            {
                "name": f"{business_type} Example {i}",
                "address": f"{location}, {country}",
                "website": None if i % 2 == 0 else "https://example.com",
                "phone": None,
                "maps_link": "https://maps.google.com",
                "score": "high" if i % 2 == 0 else "medium",
                "reason": "Demo lead (no API key)"
            }
            for i in range(1, limit + 1)
        ]

    # 🔥 Sinon → vraie API
    import requests

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

        website = result.get("website")
        phone = result.get("phone")

        if not website:
            score = "high"
            reason = "No website found, strong opportunity"
        else:
            score = "medium"
            reason = "Has website"

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
