# SPDX-FileCopyrightText: 2025-present John Yeo <johnyeocx@gmail.com>
#
# SPDX-License-Identifier: MIT

import os
from autumn.customers.cus_methods import CustomerMethods
from autumn.customers.cus_types import CreateCustomerParams, Customer
from autumn.general.types.check_types import CheckParams, CheckResult
from autumn.general.types.gen_types import CancelParams, CancelResult, TrackParams, TrackResult, UsageParams, UsageResult
from .general.types.attach_types import AttachParams, AttachResult
from .client import Autumn

secret_key = os.getenv("AUTUMN_SECRET_KEY")
api_url = "https://api.useautumn.com/v1"
api_version = "1.2"


def get_autumn() -> Autumn:
    return Autumn()


def attach(params: AttachParams) -> AttachResult:
    return get_autumn().attach(params)


def cancel(params: CancelParams) -> CancelResult:
    return get_autumn().cancel(params)


def track(params: TrackParams) -> TrackResult:
    return get_autumn().track(params)


def check(params: CheckParams) -> CheckResult:
    return get_autumn().check(params)


def usage(params: UsageParams) -> UsageResult:
    return get_autumn().usage(params)


customers = CustomerMethods()

__all__ = [
    "secret_key",
    "attach",

    # Gen Types
    "AttachParams",
    "AttachResult",
    "CancelParams",
    "CancelResult",
    "TrackParams",
    "TrackResult",
    "CheckParams",
    "CheckResult",
]
