import json
from pydantic import BaseModel


class AutumnBase(BaseModel):

    def __str__(self) -> str:
        class_name = self.__class__.__name__
        data = self.model_dump(exclude_unset=True)

        data = json.dumps(self.model_dump(exclude_unset=True), indent=4)

        return f"{class_name}({data})"
