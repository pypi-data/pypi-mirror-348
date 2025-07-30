import os
from typing import Dict, Optional, Any
import requests
from pydantic import BaseModel
from requests import Response

from autumn.error import AutumnError
from autumn.general.types.attach_types import AttachParams, AttachResult

# Constants
LATEST_API_VERSION = "1.2"
DEFAULT_API_URL = "https://api.useautumn.com/v1"
HTTP_TIMEOUT_SECONDS = 10


class Autumn:
    """
    Autumn SDK client for interacting with the Autumn API.
    
    Autumn is a layer over Stripe which makes it easy to build any pricing model.
    It controls entitlements and billing, allowing customers to define pricing models
    and manage feature access.
    """

    def __init__(self,
                 secret_key: Optional[str] = None,
                 url: Optional[str] = None,
                 version: Optional[str] = None):
        """
        Initialize the Autumn client with API credentials.
        
        Args:
            config: Complete configuration object (alternative to individual params)
            secret_key: Your Autumn secret API key
            publishable_key: Your Autumn publishable API key
            url: Base URL for the Autumn API
            version: API version to use
        """

        self.secret_key = secret_key or os.environ.get("AUTUMN_SECRET_KEY")
        self.url = url or DEFAULT_API_URL
        self.version = version or LATEST_API_VERSION

        # Validate credentials
        if not self.secret_key and not self.publishable_key:
            raise ValueError(
                "Autumn secret key or publishable key is required")

        # Setup headers and determine access level
        self.headers = {
            "Authorization":
            f"Bearer {self.secret_key or self.publishable_key}",
            "Content-Type": "application/json",
            "x-api-version": self.version
        }

        self.customers = None
        self.products = None
        self.entities = None

    def handle_response(
            self,
            response: Response,
            response_model: Optional[BaseModel] = None) -> Dict[str, Any]:

        try:
            body = response.json()
        except:
            raise AutumnError(
                message=f"Failed to parse response as JSON: {response.text}",
                code="json_parse_error",
                status_code=response.status_code)

        # Failure case
        if (response.status_code >= 300):
            error = AutumnError.from_response(response)
            raise error

        # Success case
        if response_model:
            try:
                return response_model.model_validate(body)
            except:
                raise AutumnError(
                    message=
                    f"Failed to validate response as {response_model.__name__}: {body}",
                    code="validation_error",
                    status_code=response.status_code)
        else:
            return body

    def get(self, path: str, response_model: BaseModel) -> Dict[str, Any]:
        response = requests.get(f"{self.url}{path}",
                                headers=self.headers,
                                timeout=HTTP_TIMEOUT_SECONDS)
        return self.handle_response(response, response_model)

    def post(self, path: str, body: Dict[str, Any],
             response_model: BaseModel) -> Dict[str, Any]:
        response = requests.post(f"{self.url}{path}",
                                 headers=self.headers,
                                 json=body,
                                 timeout=HTTP_TIMEOUT_SECONDS)

        return self.handle_response(response, response_model)

    def delete(self, path: str, response_model: BaseModel) -> Dict[str, Any]:
        response = requests.delete(f"{self.url}{path}",
                                   headers=self.headers,
                                   timeout=HTTP_TIMEOUT_SECONDS)

        return self.handle_response(response, response_model)

    # These instance methods will be implemented later
    def attach(self, params: AttachParams) -> AttachResult:
        return self.post(path="/attach",
                         body=params.model_dump(),
                         response_model=AttachResult)

    # def cancel(self, params):
    #     """Cancel a subscription"""
    #     pass

    # def check(self, params):
    #     """Check if a customer is entitled to a feature"""
    #     pass

    # def track(self, params):
    #     """Track an event"""
    #     pass

    # def usage(self, params):
    #     """Record usage for a feature"""
    #     pass

    # # # Static methods will be implemented after we have the proper models
    # # @classmethod
    # # def attach_static(cls, params):
    # #     """Static method to attach a customer to a product"""
    # #     pass

    # # @classmethod
    # # def cancel_static(cls, params):
    # #     """Static method to cancel a subscription"""
    # #     pass

    # # @classmethod
    # # def entitled_static(cls, params):
    # #     """Static method to check if a customer is entitled to a feature (deprecated)"""
    # #     pass

    # # @classmethod
    # # def check_static(cls, params):
    # #     """Static method to check if a customer is entitled to a feature"""
    # #     pass

    # # @classmethod
    # # def event_static(cls, params):
    # #     """Static method to track an event (deprecated)"""
    # #     pass

    # # @classmethod
    # # def track_static(cls, params):
    # #     """Static method to track an event"""
    # #     pass

    # # @classmethod
    # # def usage_static(cls, params):
    # #     """Static method to record usage for a feature"""
    # #     pass
