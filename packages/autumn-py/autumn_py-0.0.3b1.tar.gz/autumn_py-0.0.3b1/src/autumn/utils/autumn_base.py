import json
from pydantic import BaseModel


class AutumnBase(BaseModel):

    def __str__(self) -> str:
        return json.dumps(self.model_dump(), indent=4)
