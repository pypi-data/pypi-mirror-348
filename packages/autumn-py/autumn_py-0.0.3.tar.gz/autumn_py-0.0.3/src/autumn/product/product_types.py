from enum import Enum
from typing import Literal, Optional, List, Union, Any
from pydantic import BaseModel

# Enums
Infinite = "inf"


class FreeTrialDuration(str, Enum):
    Day = "day"


class UsageModel(str, Enum):
    Prepaid = "prepaid"
    PayPerUse = "pay_per_use"


UsageModelType = Literal["prepaid", "pay_per_use"]


class ProductItemInterval(str, Enum):
    Minute = "minute"
    Hour = "hour"
    Day = "day"
    Week = "week"
    Month = "month"
    Quarter = "quarter"
    SemiAnnual = "semi_annual"
    Year = "year"
    Multiple = "multiple"


ProductItemIntervalType = Literal[
    "minute",
    "hour",
    "day",
    "week",
    "month",
    "quarter",
    "semi_annual",
    "year",
    "multiple",
]


class PriceTier(BaseModel):
    to: float
    amount: Union[float, str]  # Can be a number or "inf"


class ProductItem(BaseModel):
    feature_id: Optional[str] = None
    included_usage: Optional[Union[float, str]] = None  # Infinite is "inf"
    interval: Optional[ProductItemIntervalType] = None
    usage_model: Optional[UsageModelType] = None
    price: Optional[float] = None
    billing_units: Optional[float] = None
    entity_feature_id: Optional[str] = None
    reset_usage_on_billing: Optional[bool] = None
    reset_usage_when_enabled: Optional[bool] = None


class FreeTrial(BaseModel):
    duration: FreeTrialDuration
    length: float
    unique_fingerprint: bool


class Product(BaseModel):
    autumn_id: str
    created_at: float
    id: str
    name: str
    env: Literal["sandbox", "live"]
    is_add_on: bool
    is_default: bool
    group: str
    version: float
    items: List[ProductItem]
    free_trial: Optional[FreeTrial] = None


class CreateProductParams(BaseModel):
    id: str
    name: Optional[str] = None
    is_add_on: Optional[bool] = None
    is_default: Optional[bool] = None
    items: Optional[List[ProductItem]] = None
    free_trial: Optional[FreeTrial] = None
