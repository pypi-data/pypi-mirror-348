from typing import Dict, List, Literal, Optional
from pydantic import BaseModel
from autumn.customers.cus_types import CustomerFeature, CustomerInvoice, CustomerProduct
from autumn.utils.autumn_base import AutumnBase

EntityExpandOption = Literal["invoices"]


class CreateEntityParams(AutumnBase):
    id: str
    name: str
    feature_id: str


class CreateEntityResult(AutumnBase):
    success: bool


class DeleteEntityResult(AutumnBase):
    success: bool


class GetEntityParams(AutumnBase):
    expand: Optional[List[EntityExpandOption]] = None


class Entity(AutumnBase):
    id: str
    name: str
    customer_id: str
    created_at: int
    env: str
    products: List[CustomerProduct]
    features: Dict[str, CustomerFeature]
    invoices: Optional[List[CustomerInvoice]] = None
