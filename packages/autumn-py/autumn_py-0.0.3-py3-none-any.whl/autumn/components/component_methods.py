from typing import List, Optional
from pydantic import BaseModel, validate_call

from autumn.request import Request


class PriceInfo(BaseModel):
    primaryText: str
    secondaryText: Optional[str] = None


class ItemInfo(BaseModel):
    primaryText: str
    secondaryText: Optional[str] = None


class GetPricingTableParams(BaseModel):
    customer_id: Optional[str] = None


class PricingTableProduct(BaseModel):
    id: str
    name: str
    buttonText: str
    price: PriceInfo
    items: List[ItemInfo]


class PricingTableResponse(BaseModel):
    list: List[PricingTableProduct]


class ComponentMethods:
    PricingTableParams = GetPricingTableParams

    def __init__(self,
                 api_url: Optional[str] = None,
                 secret_key: Optional[str] = None,
                 api_version: Optional[str] = None):

        self.request = Request(api_url=api_url,
                               secret_key=secret_key,
                               api_version=api_version)

    @validate_call
    def pricing_table(self,
                      params: PricingTableParams) -> PricingTableResponse:

        return self.request.get(
            path=f"/components/pricing_table?customer_id={params.customer_id}",
            response_model=PricingTableResponse)
