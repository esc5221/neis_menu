from typing import List, Optional, Any
from pydantic import BaseModel, validator

from schools.types import SchoolTypes

class SchoolSchema(BaseModel):
    id: int
    code: int
    name: str
    edu_office_code: Any
    type: Any
    location: str
    address: str

    @validator('type')
    def type_to_str(cls, type):
        return SchoolTypes(type).label