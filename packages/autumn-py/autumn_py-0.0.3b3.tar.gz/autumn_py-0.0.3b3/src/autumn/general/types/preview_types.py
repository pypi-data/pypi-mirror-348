from typing import Optional, Union, Any, Literal, List
from pydantic import BaseModel
from autumn.product.product_types import Product, UsageModelType


class CheckFeaturePreview(BaseModel):
    scenario: Literal["usage_limit", "feature_flag"]
    title: str
    message: str
    feature_id: str
    feature_name: str
    products: List[Product]


CheckProductScenario = Literal[
    "scheduled",
    "active",
    "new",
    "renew",
    "upgrade",
    "downgrade",
    "cancel",
]


class ProductPreviewItem(BaseModel):
    price: str
    description: str
    usage_model: Optional[UsageModelType] = None


class ProductPreviewOptionTier(BaseModel):
    to: Union[float, str]
    amount: float


class ProductPreviewOption(BaseModel):
    feature_id: str
    feature_name: str
    billing_units: float
    price: Optional[float] = None
    tiers: Optional[List[ProductPreviewOptionTier]] = None


class ProductPreviewDue(BaseModel):
    price: float
    currency: str


class CheckProductPreview(BaseModel):
    scenario: CheckProductScenario
    product_id: str
    product_name: str
    recurring: bool
    error_on_attach: Optional[bool] = None
    next_cycle_at: Optional[float] = None
    current_product_name: Optional[str] = None
    items: Optional[List[ProductPreviewItem]] = None
    options: Optional[List[ProductPreviewOption]] = None
    due_today: Optional[ProductPreviewDue] = None
    due_next_cycle: Optional[ProductPreviewDue] = None
