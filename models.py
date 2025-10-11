from typing import List, Optional
from pydantic import BaseModel, Field, validator
class BBox(BaseModel):
    x1: int; y1: int; x2: int; y2: int
    text: Optional[str] = None
    confidence: Optional[float] = Field(None, ge=0.0, le=100.0)
class LineItem(BaseModel):
    description: str = Field(..., min_length=1)
    quantity: float = Field(..., ge=0)
    unit_price: float = Field(..., ge=0)
    amount: float = Field(..., ge=0)
    bbox: Optional[BBox] = None
    confidence: Optional[float] = Field(None, ge=0.0, le=100.0)
class InvoiceResponse(BaseModel):
    vendor: str
    invoice_number: str
    invoice_date: str
    currency: str
    subtotal: float
    tax: float
    total: float
    line_items: List[LineItem]
    layout: Optional[List[BBox]] = None
    ocr_text: Optional[str] = None
    confidence_overall: Optional[float] = Field(None, ge=0.0, le=100.0)
    @validator("currency")
    def uppercase_currency(cls, v):
        return v.strip().upper()
    @validator("invoice_date")
    def nonempty_date(cls, v):
        v2 = v.strip()
        if not v2:
            raise ValueError("invoice_date cannot be empty")
        return v2
