# SPDX-FileCopyrightText: 2025-present John Yeo <johnyeocx@gmail.com>
#
# SPDX-License-Identifier: MIT

# from .client import Autumn

import os
from .general.types.attach_types import AttachParams, AttachResult
from .client import Autumn

api_key = os.getenv("AUTUMN_API_KEY")


def get_autumn() -> Autumn:
    return Autumn(api_key)


def attach(params: AttachParams) -> AttachResult:
    return get_autumn().attach(params)


# Expose in __all__ for clarity
# Import types

__all__ = [
    "api_key",
    "attach",

    # Types
    "AttachParams",
    "AttachResult",
]
