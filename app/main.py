from fastapi import FastAPI, HTTPException
from app.models.schemas import LeadSearchRequest, LeadSearchResponse
from app.services.lead_finder import find_leads
from app.core.settings import SERP_API_KEY

app = FastAPI(title="LeadFlow API")


@app.get("/")
def root():
    return {"message": "LeadFlow API is running"}


@app.post("/find-leads", response_model=LeadSearchResponse)
def get_leads(request: LeadSearchRequest):
    if not SERP_API_KEY:
        raise HTTPException(status_code=500, detail="SERP_API_KEY is missing")

    try:
        leads = find_leads(
            target_business_type=request.target_business_type,
            location=request.location,
            country=request.country,
            limit=request.lead_count,
        )
        return {"leads": leads}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lead search failed: {str(e)}")
