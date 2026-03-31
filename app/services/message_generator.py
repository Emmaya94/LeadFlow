import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_message(user_business, offer_summary, lead, language="en", tone="professional"):

    # 🔥 fallback si pas de clé OpenAI
    if not os.getenv("OPENAI_API_KEY"):
        return f"Hi, I came across {lead['name']} and thought my {user_business} service could help your business."

    prompt = f"""
You are helping a freelancer contact a business.

User business: {user_business}
Offer: {offer_summary}

Target business:
Name: {lead.get("name")}
Location: {lead.get("address")}

Write a short outreach message in {language}.

Tone: {tone}

Rules:
- Keep it natural (not spammy)
- Make it feel human
- Mention something relevant (like local business)
- Keep it under 80 words
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()
