from typing import Optional
from autumn.client import Autumn
from autumn.error import AutumnError
from autumn.general.types.gen_types import CustomerDataParams
from autumn.router.create_router import create_router
from autumn.router.with_auth import AuthResult, WithAuthParams


async def get_body(request):
    return await request.json() if request.method in ["POST", "PUT", "PATCH"
                                                      ] else {}


async def autumn_handler(request,
                         customer_id: Optional[str] = None,
                         customer_data: Optional[CustomerDataParams] = None):

    from fastapi.responses import JSONResponse
    from fastapi.logger import logger

    url = request.url
    pathname = url.path
    query_params = dict(request.query_params)

    router = create_router()
    handler, path_params = router.match(request.method, pathname)

    if handler:
        try:
            body = await get_body(request)
        except Exception as e:
            print("[Autumn Handler Error] Invalid JSON")
            return JSONResponse(content={
                "message": "Invalid JSON",
                "code": "invalid_json"
            },
                                status_code=400)

        def get_customer():
            return AuthResult(customer_id=customer_id,
                              customer_data=customer_data)

        autumn = Autumn()

        params = WithAuthParams(autumn=autumn,
                                body=body,
                                path=pathname,
                                get_customer=get_customer,
                                path_params=path_params,
                                search_params=query_params)

        result = await handler(params)
        if isinstance(result.data, AutumnError):
            return JSONResponse(content=result.data.to_dict(),
                                status_code=result.status_code or 500)
        else:
            return JSONResponse(content=result.data,
                                status_code=result.status_code)

    return JSONResponse(content={"message": f"{pathname} not found"},
                        status_code=404)


__all__ = ["autumn_handler"]
