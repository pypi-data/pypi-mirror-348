from typing import Optional
from requests import Response


class AutumnError(Exception):
    """Base exception for Autumn SDK errors"""

    def __init__(self,
                 message: str = "Unknown error occurred",
                 code: str = "unknown_error",
                 status_code: Optional[int] = None):

        self.message = message
        self.code = code
        self.status_code = status_code

        super().__init__(self.message)

    @classmethod
    def from_response(cls, response: Response):
        try:

            response_json = response.json()

            return cls(message=response_json.get('message',
                                                 'Unknown error occurred'),
                       code=response_json.get('code', 'unknown_error'),
                       status_code=response.status_code)
        except (ValueError, AttributeError) as e:

            return cls(message=response.text,
                       code="unknown_error",
                       status_code=response.status_code)

    def __str__(self):
        return f"Autumn Error ({self.code}): {self.message}"
