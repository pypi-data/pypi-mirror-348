from autumn.router.constants import BASE_PATH
from autumn.router.router import RouteHandlerParams, Router
from autumn.router.with_auth import with_auth


@with_auth
def attach(params: RouteHandlerParams):
    autumn = params.autumn

    result = autumn.attach({
        "customer_id": params.customer_id,
        "customer_data": params.customer_data,
        **params.body
    }).model_dump(exclude_unset=True)

    return result


@with_auth
def check(params: RouteHandlerParams):
    autumn = params.autumn

    result = autumn.check({
        "customer_id": params.customer_id,
        "customer_data": params.customer_data,
        **params.body
    }).model_dump(exclude_unset=True)

    return result


@with_auth
def track(params: RouteHandlerParams):
    autumn = params.autumn

    result = autumn.track({
        "customer_id": params.customer_id,
        "customer_data": params.customer_data,
        **params.body
    }).model_dump(exclude_unset=True)

    return result


@with_auth
def cancel(params: RouteHandlerParams):
    autumn = params.autumn

    result = autumn.cancel({
        "customer_id": params.customer_id,
        **params.body
    }).model_dump(exclude_unset=True)

    return result


@with_auth
def billing_portal(params: RouteHandlerParams):
    autumn = params.autumn

    result = autumn.customers.billing_portal(id=params.customer_id,
                                             params={
                                                 **params.body,
                                             }).model_dump(exclude_unset=True)

    return result


def create_gen_routes(router: Router):
    router.add_route(
        "POST",
        f"{BASE_PATH}/attach",
        attach,
    )

    router.add_route(
        "POST",
        f"{BASE_PATH}/check",
        check,
    )

    router.add_route(
        "POST",
        f"{BASE_PATH}/track",
        track,
    )

    router.add_route(
        "POST",
        f"{BASE_PATH}/cancel",
        cancel,
    )

    router.add_route(
        "POST",
        f"{BASE_PATH}/billing_portal",
        billing_portal,
    )
