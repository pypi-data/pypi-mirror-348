import re
from typing import Callable, Dict, Optional, Tuple, List, Any

from pydantic import BaseModel

from autumn.client import Autumn
from autumn.customers.cus_types import CustomerDataParams


class RouteHandlerParams(BaseModel):
    model_config = {"arbitrary_types_allowed": True}

    autumn: Autumn
    body: Dict[str, Any]
    customer_id: Optional[str] = None
    customer_data: Optional[CustomerDataParams] = None
    path_params: Optional[Dict[str, str]] = None
    search_params: Optional[Dict[str, str]] = None


class Route:

    def __init__(self, method: str, path_pattern: str, handler: Callable,
                 **options):
        self.method = method.upper()
        self.path_pattern = path_pattern
        self.handler = handler
        self.options = options

        # Convert Express/FastAPI style path params (e.g., /users/{id}) to regex pattern
        # Replace <param> with named capture groups (?P<param>[^/]+)
        regex_pattern = re.sub(r'<([^/]+)>', r'(?P<\1>[^/]+)', path_pattern)
        # Add start/end anchors and make trailing slash optional
        self.regex = re.compile(f"^{regex_pattern}/?$")


class Router:

    def __init__(self):
        self.routes: List[Route] = []

    def add_route(self, method: str, path: str, handler: Callable,
                  **options) -> 'Router':
        """Register a route with the router."""
        self.routes.append(Route(method, path, handler, **options))
        return self

    def match(self, method: str,
              pathname: str) -> Tuple[Optional[Callable], Dict[str, str]]:
        """
        Match a pathname against registered routes.
        
        Returns:
            Tuple containing (handler_function, path_params)
            If no match is found, handler will be None
        """
        method = method.upper()

        for route in self.routes:
            if route.method != method:
                continue

            match = route.regex.match(pathname)
            if match:
                # Extract path parameters from the regex match
                path_params = match.groupdict()
                return route.handler, path_params

        # No match found
        return None, {}

    def handle_request(self, method: str, pathname: str, *args,
                       **kwargs) -> Any:
        """
        Handle a request with the given method and pathname.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            pathname: URL path to match
            *args, **kwargs: Additional arguments to pass to the handler
            
        Returns:
            Result from the handler function or None if no route matches
        """
        handler, path_params = self.match(method, pathname)

        if handler:
            # Merge path_params with any other kwargs
            kwargs.update(path_params)
            return handler(*args, **kwargs)

        return None
