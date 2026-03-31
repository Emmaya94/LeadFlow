import os
import requests
from app.services.message_generator import generate_message

SERP_API_KEY = os.getenv("SERP_API_KEY")


def find_leads(business_type, location, country, limit=5):

    # 🔥 MODE DEMO si pas de clé API
    if not SERP_API_KEY:
        leads = []

        for i in range(1, limit + 1):
            lead = {
                "name": f"{business_type} Example {i}",
                "address": f"{location}, {country}",
                "website": None if i % 2 == 0 else "https://example.com",
                "phone": None,
                "maps_link": "https://maps.google.com"
            }

            # scoring
            if not lead["website"]:
                score = "high"
                reason = "No website found, strong opportunity"
            else:
                score = "medium"
                reason = "Has website"

            # message
            message = generate_message(
                user_business=business_type,
                offer_summary=f"I help {business_type} businesses grow",
                lead=lead,
                language="en",
                tone="professional"
            )

            lead.update({
                "score": score,
                "reason": reason,
                "message": message
            })

            leads.append(lead)

        return leads

    # 🔥 MODE RÉEL (SerpAPI)
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

        lead = {
            "name": result.get("title"),
            "address": result.get("address"),
            "website": result.get("website"),
            "phone": result.get("phone"),
            "maps_link": result.get("link")
        }

        # scoring
        if not lead["website"]:
            score = "high"
            reason = "No website found, strong opportunity"
        elif lead["website"] and not lead["phone"]:
            score = "medium"
            reason = "Has website but limited contact info"
        else:
            score = "low"
            reason = "Has website and contact info"

        # message
        message = generate_message(
            user_business=business_type,
            offer_summary=f"I help {business_type} businesses grow",
            lead=lead,
            language="en",
            tone="professional"
        )

        lead.update({
            "score": score,
            "reason": reason,
            "message": message
        })

        leads.append(lead)

    return leads
