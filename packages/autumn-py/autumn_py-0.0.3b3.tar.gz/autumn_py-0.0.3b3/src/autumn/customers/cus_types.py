from typing import Literal, Optional, List, Dict, Any
from enum import Enum

from autumn.product.product_types import ProductItemIntervalType
from autumn.utils.autumn_base import AutumnBase


class CustomerFeature(AutumnBase):
    id: str
    name: str
    unlimited: Optional[bool] = None
    interval: Optional[ProductItemIntervalType] = None
    balance: Optional[float] = None
    usage: Optional[float] = None
    included_usage: Optional[float] = None
    next_reset_at: Optional[int] = None
    breakdown: Optional[List[Dict[str, Any]]] = None


class ProductStatus(str, Enum):
    Active = "active"
    Expired = "expired"
    Trialing = "trialing"
    Scheduled = "scheduled"


class CustomerProduct(AutumnBase):
    id: str
    name: Optional[str] = None
    group: Optional[str] = None
    status: ProductStatus
    started_at: int
    canceled_at: Optional[int] = None
    subscription_ids: Optional[List[str]] = None
    current_period_start: Optional[int] = None
    current_period_end: Optional[int] = None


class Customer(AutumnBase):
    id: Optional[str] = None
    created_at: int
    name: Optional[str] = None
    email: Optional[str] = None
    fingerprint: Optional[str] = None
    stripe_id: Optional[str] = None
    env: str  # Assuming AppEnv is a string enum
    metadata: Dict[str, Any]
    products: List[CustomerProduct]
    features: Dict[str, CustomerFeature]
    invoices: Optional[List['CustomerInvoice']] = None


class CustomerDataParams(AutumnBase):
    name: Optional[str] = None
    email: Optional[str] = None
    fingerprint: Optional[str] = None


CustomerExpandOption = Literal["invoices", "rewards", "trials_used"]


class GetCustomerParams(AutumnBase):
    expand: Optional[List[CustomerExpandOption]] = None


class CreateCustomerParams(AutumnBase):
    id: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    fingerprint: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    expand: Optional[List[CustomerExpandOption]] = None


class UpdateCustomerParams(AutumnBase):
    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    fingerprint: Optional[str] = None


class BillingPortalParams(AutumnBase):
    return_url: Optional[str] = None


class BillingPortalResponse(AutumnBase):
    customer_id: str
    url: str


class CustomerInvoice(AutumnBase):
    product_ids: List[str]
    stripe_id: str
    status: str
    total: float
    currency: str
    created_at: int


class BillingPortalParams(AutumnBase):
    return_url: Optional[str] = None


class BillingPortalResponse(AutumnBase):
    customer_id: Optional[str] = None
    url: str
