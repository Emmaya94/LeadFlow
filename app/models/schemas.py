
from pydantic import BaseModel, Field
from typing import List, Optional


class LeadSearchRequest(BaseModel):
    target_business_type: str = Field(..., min_length=2)
    country: str = Field(..., min_length=2)
    location: str = Field(..., min_length=2)
    lead_count: int = Field(default=5, ge=1, le=20)


class LeadItem(BaseModel):
    name: str
    address: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    maps_link: Optional[str] = None


class LeadSearchResponse(BaseModel):
    leads: List[LeadItem]