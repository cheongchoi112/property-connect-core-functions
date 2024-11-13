from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class PropertyBase(BaseModel):
    """
    Domain Layer: Base model for property data.
    """
    description: str
    price: float
    street_address: str
    city: str
    property_type: str
    listing_type: str

class PropertyCreate(PropertyBase):
    """
    Domain Layer: Model for creating a new property.
    """
    pass

class PropertyUpdate(PropertyBase):
    """
    Domain Layer: Model for updating an existing property.
    """
    pass

class Property(PropertyBase):
    """
    Domain Layer: Model representing a property.
    """
    id: str
    owner_user_id: str
    owner_email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        frozen = True  # This makes the model immutable and hashable

class PriceRange(BaseModel):
    """
    Domain Layer: Model representing a price range.
    """
    min_price: float
    max_price: float

class SearchCriteria(BaseModel):
    """
    Domain Layer: Model representing search criteria for properties.
    """
    city: Optional[str] = None
    price_range: Optional[PriceRange] = None
    property_type: Optional[str] = None
    listing_type: Optional[str] = None