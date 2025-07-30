from autumn.entities.entity_types import GetEntityParams
from autumn.router.constants import BASE_PATH
from autumn.router.router import RouteHandlerParams, Router
from autumn.router.with_auth import with_auth


@with_auth
def create_entity(params: RouteHandlerParams):
    autumn = params.autumn
    customer_id = params.customer_id
    body = params.body

    return autumn.entities.create(customer_id,
                                  body).model_dump(exclude_unset=True)


@with_auth
def get_entity(params: RouteHandlerParams):
    autumn = params.autumn
    customer_id = params.customer_id
    entity_id = params.path_params["entity_id"]
    search_params = params.search_params

    expand = search_params.get("expand",
                               []).split(",") if search_params else None

    entity = autumn.entities.get(customer_id,
                                 entity_id,
                                 params=GetEntityParams(expand=expand))

    return entity.model_dump(exclude_unset=True)


@with_auth
def delete_entity(params: RouteHandlerParams):
    autumn = params.autumn
    customer_id = params.customer_id
    entity_id = params.path_params["entity_id"]

    return autumn.entities.delete(customer_id, entity_id)


def create_ent_routes(router: Router):
    router.add_route("POST", f"{BASE_PATH}/entities", create_entity)
    router.add_route("GET", f"{BASE_PATH}/entities/<entity_id>", get_entity)
    router.add_route("DELETE", f"{BASE_PATH}/entities/<entity_id>",
                     delete_entity)
