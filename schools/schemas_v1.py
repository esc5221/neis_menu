from typing import List, Optional, Any
from pydantic import BaseModel, validator

from schools.types import SchoolTypes

class SchoolSchema(BaseModel):
    '''
    학교 정보를 담고 있는 모델
    '''
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