from typing import Optional
from pydantic import validate_call

from autumn.components.component_methods import ComponentMethods
from autumn.customers.cus_methods import CustomerMethods
from autumn.entities.entity_methods import EntityMethods
from autumn.general.types.attach_types import AttachParams, AttachResult
from autumn.general.types.check_types import CheckParams, CheckResult
from autumn.general.types.gen_types import CancelParams, CancelResult, TrackParams, TrackResult, UsageParams, UsageResult

from autumn.request import Request

# Constants
LATEST_API_VERSION = "1.2"
DEFAULT_API_URL = "https://api.useautumn.com/v1"


class Autumn:
    """
    Autumn SDK client for interacting with the Autumn API.
    
    Autumn is a layer over Stripe which makes it easy to build any pricing model.
    It controls entitlements and billing, allowing customers to define pricing models
    and manage feature access.
    """

    def __init__(self,
                 secret_key: Optional[str] = None,
                 api_url: Optional[str] = None,
                 api_version: Optional[str] = None):
        """
        Initialize the Autumn client with API credentials.
        
        Args:
            config: Complete configuration object (alternative to individual params)
            secret_key: Your Autumn secret API key
            publishable_key: Your Autumn publishable API key
            url: Base URL for the Autumn API
            version: API version to use
        """

        self.secret_key = secret_key
        self.api_url = api_url
        self.api_version = api_version

        self.request = Request(api_url=self.api_url,
                               secret_key=self.secret_key,
                               api_version=self.api_version)

        self.customers = CustomerMethods(api_url=self.api_url,
                                         secret_key=self.secret_key,
                                         api_version=self.api_version)

        self.products = None
        self.entities = EntityMethods(api_url=self.api_url,
                                      secret_key=self.secret_key,
                                      api_version=self.api_version)
        self.components = ComponentMethods(api_url=self.api_url,
                                           secret_key=self.secret_key,
                                           api_version=self.api_version)

    # These instance methods will be implemented later
    @validate_call
    def attach(self, params: AttachParams) -> AttachResult:

        result = self.request.post(path="/attach",
                                   params=params.model_dump(),
                                   response_model=AttachResult)

        return result

    @validate_call
    def cancel(self, params: CancelParams) -> CancelResult:
        """Cancel a subscription"""
        return self.request.post(path="/cancel",
                                 params=params.model_dump(),
                                 response_model=CancelResult)

    @validate_call
    def track(self, params: TrackParams) -> TrackResult:
        """Track an event"""
        return self.request.post(path="/track",
                                 params=params.model_dump(),
                                 response_model=TrackResult)

    @validate_call
    def check(self, params: CheckParams) -> CheckResult:
        """Check if a customer is entitled to a feature"""
        check_result = self.request.post(path="/check",
                                         params=params.model_dump(),
                                         response_model=CheckResult)

        return check_result

    @validate_call
    def usage(self, params: UsageParams) -> UsageResult:
        """Record usage for a feature"""
        return self.request.post(path="/usage",
                                 params=params.model_dump(),
                                 response_model=UsageResult)
