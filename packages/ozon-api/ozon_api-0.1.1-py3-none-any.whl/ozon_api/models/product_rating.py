from typing import List, Optional
from pydantic import BaseModel

class ProductRatingGroup(BaseModel):
    name: str
    rating: float
    recommendations: Optional[List[str]] = None

class ProductRatingItem(BaseModel):
    sku: int
    rating: float
    groups: List[ProductRatingGroup]

class ProductRatingRequest(BaseModel):
    skus: List[int]

class ProductRatingResponse(BaseModel):
    products: List[ProductRatingItem] 