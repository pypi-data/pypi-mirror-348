from pydantic import BaseModel
from typing import Optional, List, Dict
from autumn.general.types.gen_types import CustomerDataParams
from autumn.utils.autumn_base import AutumnBase


class AttachOptionParams(BaseModel):
    feature_id: str
    quantity: int


class AttachParams(BaseModel):
    customer_id: str

    product_id: Optional[str] = None
    entity_id: Optional[str] = None
    options: Optional[List[AttachOptionParams]] = None
    product_ids: Optional[List[str]] = None
    free_trial: Optional[bool] = None
    success_url: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
    force_checkout: Optional[bool] = None
    customer_data: Optional[CustomerDataParams] = None


class AttachResult(AutumnBase):
    customer_id: str
    product_ids: List[str]
    code: str = "no code returned"
    message: str = "no message returned"
    checkout_url: Optional[str] = None
