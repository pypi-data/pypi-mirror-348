from typing import Optional
from pydantic import BaseModel


class CustomerDataParams(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    fingerprint: Optional[str] = None
