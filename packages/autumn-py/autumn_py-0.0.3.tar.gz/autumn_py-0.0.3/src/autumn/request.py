import json
from typing import Any, Dict, Generic, Optional
import requests
from typing_extensions import Literal, TypeVar
from pydantic import BaseModel

import autumn
from autumn.error import AutumnError

HTTP_TIMEOUT_SECONDS = 10

RequestVerb = Literal["get", "post", "put", "patch", "delete"]

T = TypeVar("T")


# This class wraps the HTTP request creation logic
class Request(Generic[T]):
    api_url: Optional[str]
    secret_key: Optional[str]
    api_version: Optional[str]

    def __init__(self,
                 api_url: Optional[str] = None,
                 secret_key: Optional[str] = None,
                 api_version: Optional[str] = None):

        self.api_url = api_url
        self.secret_key = secret_key
        self.api_version = api_version

    def __get_headers(self) -> Dict[Any, Any]:

        secret_key = self.secret_key or autumn.secret_key
        if not secret_key:
            raise AutumnError(
                message="Secret key is required",
                code="secret_key_required",
            )

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {secret_key}",
            "x-api-version": self.api_version or autumn.api_version or "1.2",
        }

        return headers

    def handle_response(self,
                        response: requests.Response,
                        response_model: Optional[BaseModel] = None) -> Any:
        try:
            body = response.json()
        except Exception:
            raise AutumnError(
                message=f"Failed to parse response as JSON: {response.text}",
                code="json_parse_error",
                status_code=response.status_code,
            )
        if response.status_code >= 300:
            error = AutumnError.from_response(response)
            raise error
        if response_model:
            try:
                return response_model.model_validate(body)
            except Exception as e:
                raise AutumnError(
                    message=
                    f"Failed to validate response as {response_model.__class__.__name__}:\n{e}\n\n{json.dumps(body, indent=4)}\n",
                    code="validation_error",
                    status_code=response.status_code,
                )
        else:
            return body

    def request(self,
                path: str,
                params: Optional[Dict[Any, Any]] = None,
                verb: RequestVerb = "get",
                response_model: Optional[BaseModel] = None) -> Any:

        base_url = self.api_url or autumn.api_url
        url = f"{base_url}{path}"

        headers = self.__get_headers()

        try:
            response = requests.request(
                method=verb,
                url=url,
                json=params,
                headers=headers,
                timeout=HTTP_TIMEOUT_SECONDS,
            )
        except requests.RequestException as e:
            raise AutumnError(message=str(e), code="request_exception")
        return self.handle_response(response, response_model)

    def get(self,
            path: str,
            response_model: Optional[BaseModel] = None) -> Any:

        return self.request(path=path,
                            verb="get",
                            response_model=response_model)

    def post(self,
             path: str,
             params: Optional[Dict[Any, Any]] = None,
             response_model: Optional[BaseModel] = None) -> Any:

        return self.request(path=path,
                            params=params,
                            verb="post",
                            response_model=response_model)

    def delete(self,
               path: str,
               response_model: Optional[BaseModel] = None) -> Any:
        return self.request(path=path,
                            verb="delete",
                            response_model=response_model)
