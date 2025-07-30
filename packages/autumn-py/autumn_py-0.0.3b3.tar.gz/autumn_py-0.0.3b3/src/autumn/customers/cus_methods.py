from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, validate_call

from autumn.customers.cus_types import BillingPortalParams, BillingPortalResponse, CreateCustomerParams, Customer, CustomerExpandOption, GetCustomerParams, UpdateCustomerParams
from autumn.request import Request


class CustomerMethodsInterface(BaseModel):
    create: Callable[[CreateCustomerParams], Customer]


def get_query_params(
        expand: Optional[List[CustomerExpandOption]] = None) -> Dict[str, Any]:

    if expand:
        return f"expand={','.join([option for option in expand])}"

    return ""


class CustomerMethods:
    CreateCustomerParams = CreateCustomerParams

    # Customer = Customer

    def __init__(self,
                 api_url: Optional[str] = None,
                 secret_key: Optional[str] = None,
                 api_version: Optional[str] = None):

        self.request = Request(api_url=api_url,
                               secret_key=secret_key,
                               api_version=api_version)

    @validate_call
    def create(self, params: CreateCustomerParams) -> Customer:
        return self.request.post(path="/customers",
                                 params=params.model_dump(),
                                 response_model=Customer)

    @validate_call
    def get(self,
            id: str,
            params: Optional[GetCustomerParams] = None) -> Customer:

        query_params = get_query_params(params.expand) if params else ""

        return self.request.get(path=f"/customers/{id}?{query_params}",
                                response_model=Customer)

    @validate_call
    def update(self, id: str, params: UpdateCustomerParams) -> Customer:
        json_params = params.model_dump(exclude_unset=True)
        return self.request.post(path=f"/customers/{id}",
                                 params=json_params,
                                 response_model=Customer)

    @validate_call
    def delete(self, id: str) -> Dict[str, Any]:
        return self.request.delete(path=f"/customers/{id}",
                                   response_model=None)

    @validate_call
    def billing_portal(self, id: str,
                       params: BillingPortalParams) -> BillingPortalResponse:
        return self.request.post(path=f"/customers/{id}/billing_portal",
                                 params=params.model_dump(),
                                 response_model=BillingPortalResponse)
