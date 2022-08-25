from typing import Optional, List
from pydantic import validator

from ninja import Schema, ModelSchema

from schools.models import School
from schools.types import SchoolTypes


class SchoolDTO(ModelSchema):
    class Config:
        model = School
        model_fields = [
            "id",
            "code",
            "name",
            "location",
            "address",
            "type",
            "edu_office_code",
        ]

    @validator("type", check_fields=False)
    def type_to_str(cls, type):
        return SchoolTypes(type).name


class SchoolListDTO(Schema):
    # objects에서 items로 변경 (django-ninja pagination과의 일관성 유지)
    items: List[SchoolDTO]


class SchoolPostParams(Schema):
    school_code: int
