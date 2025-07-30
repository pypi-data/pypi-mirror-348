import functools
from typing import Any, Callable, Dict, Optional, TypeVar, Union
from pydantic import BaseModel

from autumn.customers.cus_types import CustomerDataParams
from autumn.error import AutumnError
from autumn.router.router import RouteHandlerParams


# Type definitions using Pydantic
class AuthResult(BaseModel):
    customer_id: Optional[str] = None
    customer_data: Optional[Union[CustomerDataParams, Dict[str, Any]]] = None


class BackendError(BaseModel):
    path: str
    message: str
    code: str
    status_code: int = 500


# Parameter class for with_auth wrapper
class WithAuthParams(BaseModel):
    autumn: Any
    body: Dict[str, Any]
    path: str
    get_customer: Callable[[], AuthResult]
    path_params: Dict[str, str] = {}
    search_params: Dict[str, str] = {}


class HandlerResult(BaseModel):
    data: Any
    status_code: int


# The decorator function
def with_auth(fn=None, *, require_customer=True):
    """
    Authentication decorator for Autumn handlers.
    
    Args:
        fn: The function to decorate
        require_customer: Whether a customer ID is required
    
    Usage:
        @with_auth
        async def create_customer(autumn, customer_id, customer_data=None, **kwargs):
            # Implementation
            
        @with_auth(require_customer=False)
        async def pricing_table(autumn, customer_id=None, **kwargs):
            # Implementation
    """

    def decorator(handler_func):

        @functools.wraps(handler_func)
        async def wrapper(params: WithAuthParams):
            # Get authentication result
            auth_result = params.get_customer()

            customer_id = auth_result.customer_id if auth_result else None
            error_on_not_found = params.body.get("error_on_not_found", True)

            if not customer_id and require_customer:
                if error_on_not_found == False:
                    return HandlerResult(data={
                        "message": "No customer ID found",
                    },
                                         status_code=200)
                else:
                    return HandlerResult(data=AutumnError(
                        message="No customer ID found", code="no_customer_id"),
                                         status_code=401)

            # Call the handler function
            handler_params = RouteHandlerParams(
                autumn=params.autumn,
                body=params.body,
                customer_id=auth_result.customer_id if auth_result else None,
                customer_data=auth_result.customer_data
                if auth_result else None,
                path_params=params.path_params,
                search_params=params.search_params)

            try:
                result = handler_func(handler_params)
                return HandlerResult(data=result, status_code=200)

            except AutumnError as error:
                print("[Autumn Handler Error] ", error)
                return HandlerResult(data=error,
                                     status_code=error.status_code or 500)

            except Exception as error:
                print("[Autumn Handler Error] ", error)
                raise AutumnError(message=str(error)
                                  or f"Failed to handle route {params.path}",
                                  code="route_handler_error")

        return wrapper

    # Handle both @with_auth and @with_auth(require_customer=...)
    if fn is None:
        return decorator
    return decorator(fn)
