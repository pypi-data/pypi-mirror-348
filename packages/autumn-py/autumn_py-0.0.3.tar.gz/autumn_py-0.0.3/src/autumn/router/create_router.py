from typing import Any, Dict, Optional

from pydantic import BaseModel
from autumn.client import Autumn
from autumn.customers.cus_types import CustomerDataParams
from autumn.router.ent_routes import create_ent_routes
from autumn.router.gen_routes import create_gen_routes
from autumn.router.router import RouteHandlerParams, Router
from autumn.router.with_auth import with_auth


def sanitize_body(body: Dict[str, Any]) -> Dict[str, Any]:
    sanitized_body = {**body}
    if 'id' in sanitized_body:
        del sanitized_body['id']
    if 'name' in sanitized_body:
        del sanitized_body['name']
    if 'email' in sanitized_body:
        del sanitized_body['email']
    return sanitized_body


@with_auth
def create_customer(params: RouteHandlerParams):

    sanitized_body = sanitize_body(params.body)

    res = params.autumn.customers.create({
        "id":
        params.customer_id,
        **(params.customer_data.model_dump() if params.customer_data else {}),
        **sanitized_body
    })

    return res.model_dump(exclude_unset=True)


@with_auth(require_customer=False)
def pricing_table(params: RouteHandlerParams):
    res = params.autumn.components.pricing_table(
        {"customer_id": params.customer_id})
    return res.model_dump(exclude_unset=True)


def create_router():
    router = Router()

    # Register the route with the handler
    # The handler is already decorated with with_auth
    router.add_route(
        "POST",
        "/api/autumn/customers",
        create_customer,
    )

    router.add_route(
        "GET",
        "/api/autumn/components/pricing_table",
        pricing_table,
    )

    create_gen_routes(router)
    create_ent_routes(router)

    return router
