from typing import Any, Literal, Optional, Union
from pydantic import BaseModel
from autumn.general.types.gen_types import CustomerDataParams
from autumn.general.types.preview_types import CheckFeaturePreview, CheckProductPreview


class CheckParams(BaseModel):
    customer_id: str
    feature_id: Optional[str] = None
    product_id: Optional[str] = None
    entity_id: Optional[str] = None
    customer_data: Optional[CustomerDataParams] = None
    required_quantity: Optional[float] = None
    send_event: Optional[bool] = None
    with_preview: Optional[Union[bool, Literal["formatted", "raw"]]] = None


class CheckResult(BaseModel):
    customer_id: str  # Customer ID
    allowed: bool  # Whether the customer is allowed to use the feature
    code: str  # Success code
    feature_id: Optional[str] = None  # Feature ID
    required_quantity: Optional[
        float] = None  # Required quantity for the feature
    unlimited: Optional[bool] = None  # Whether the feature is unlimited
    balance: Optional[float] = None  # Balance for the feature
    product_id: Optional[str] = None  # Product ID
    status: Optional[str] = None  # Status of the product
    # preview: Optional[Union[CheckProductPreview, CheckFeaturePreview]] = None
    preview: Optional[Any] = None
