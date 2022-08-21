from typing import Optional, List

from ninja import Schema, ModelSchema

from schools.models import School


class SchoolDTO(ModelSchema):
    class Config:
        model = School
        model_fields = ['id', 'code', 'name', 'location']


class SchoolListDTO(Schema):
    # objects에서 items로 변경 (django-ninja pagination과의 일관성 유지)
    items: List[SchoolDTO]
