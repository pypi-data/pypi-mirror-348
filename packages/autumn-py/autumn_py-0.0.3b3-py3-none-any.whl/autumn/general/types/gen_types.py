from typing import Optional
from pydantic import BaseModel

from autumn.customers.cus_types import CustomerDataParams


class CancelParams(BaseModel):
    customer_id: str
    product_id: str
    entity_id: Optional[str] = None


class CancelResult(BaseModel):
    success: bool
    customer_id: str
    product_id: str


class TrackParams(BaseModel):
    customer_id: str
    feature_id: Optional[str] = None
    event_name: Optional[str] = None
    entity_id: Optional[str] = None

    value: Optional[float] = None
    customer_data: Optional[CustomerDataParams] = None
    idempotency_key: Optional[str] = None


class TrackResult(BaseModel):
    id: str  # Event ID
    code: str  # Success code
    customer_id: str  # Customer ID
    feature_id: Optional[str] = None  # Feature ID
    event_name: Optional[str] = None  # Event name


class UsageParams(BaseModel):
    customer_id: str
    feature_id: str
    value: float
    customer_data: Optional[CustomerDataParams] = None


class UsageResult(BaseModel):
    code: str  # Success code
    customer_id: str  # Customer ID
    feature_id: str  # Feature ID
