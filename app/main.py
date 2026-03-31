from fastapi import FastAPI
from app.services.lead_finder import find_leads

app = FastAPI()

@app.get("/")
def root():
    return {"message": "LeadFlow is running"}

@app.get("/find-leads")
def get_leads(
    business_type: str,
    location: str,
    country: str = "France",
    limit: int = 5
):
    leads = find_leads(business_type, location, country, limit)
    return {"leads": leads}
