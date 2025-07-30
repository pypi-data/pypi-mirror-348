from typing import List, Optional, Union
from pydantic import BaseModel, validate_call

from autumn.entities.entity_types import (
    CreateEntityParams,
    CreateEntityResult,
    DeleteEntityResult,
    Entity,
    EntityExpandOption,
    GetEntityParams,
)
from autumn.request import Request


def get_query_params(expand: Optional[List[EntityExpandOption]] = None) -> str:
    if expand:
        return f"expand={','.join([option for option in expand])}"
    return ""


class EntityMethods:
    CreateEntityParams = CreateEntityParams

    def __init__(
        self,
        api_url: Optional[str] = None,
        secret_key: Optional[str] = None,
        api_version: Optional[str] = None,
    ):
        self.request = Request(
            api_url=api_url,
            secret_key=secret_key,
            api_version=api_version,
        )

    @validate_call
    def get(
        self,
        customer_id: str,
        entity_id: str,
        params: Optional[GetEntityParams] = None,
    ) -> Entity:
        query_params = get_query_params(params.expand) if params else ""

        result = self.request.get(
            path=
            f"/customers/{customer_id}/entities/{entity_id}?{query_params}",
            response_model=Entity,
        )

        return result

    @validate_call
    def create(
        self,
        customer_id: str,
        params: Union[CreateEntityParams, List[CreateEntityParams]],
    ) -> Union[CreateEntityResult, List[CreateEntityResult]]:
        return self.request.post(
            path=f"/customers/{customer_id}/entities",
            params=params.model_dump()
            if isinstance(params, CreateEntityParams) else
            [p.model_dump() for p in params],
            response_model=Union[CreateEntityResult, List[CreateEntityResult]],
        )

    @validate_call
    def delete(
        self,
        customer_id: str,
        entity_id: str,
    ) -> DeleteEntityResult:
        return self.request.delete(
            path=f"/customers/{customer_id}/entities/{entity_id}",
            response_model=None,
        )
