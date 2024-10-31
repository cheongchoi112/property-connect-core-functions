from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class PropertyBase(BaseModel):
    id: str
    title: str
    description: str
    price: float
    address: str
    property_type: str
    listing_type: str

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(PropertyBase):
    pass

class Property(PropertyBase):
    owner_user_id: str
    created_at: datetime
    updated_at: datetime

class Location(BaseModel):
    latitude: float
    longitude: float
    radius: float = Field(default=5.0, description="Search radius in kilometers")

class PriceRange(BaseModel):
    min_price: float
    max_price: float

class SearchCriteria(BaseModel):
    keyword: Optional[str] = None
    location: Optional[Location] = None
    price_range: Optional[PriceRange] = None
    property_type: Optional[str] = None