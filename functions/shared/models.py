from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class PropertyBase(BaseModel):
    description: str
    price: float
    street_address: str
    city: str
    property_type: str
    listing_type: str

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(PropertyBase):
    pass

class Property(PropertyBase):
    id: str
    owner_user_id: str
    owner_email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        frozen = True  # This makes the model immutable and hashable

class PriceRange(BaseModel):
    min_price: float
    max_price: float

class SearchCriteria(BaseModel):
    city: Optional[str] = None
    price_range: Optional[PriceRange] = None
    property_type: Optional[str] = None
    listing_type: Optional[str] = None