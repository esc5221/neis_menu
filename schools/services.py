from typing import Tuple

from ninja.responses import codes_4xx

from django.db import IntegrityError

from schools.scripts.crawl_schools import get_school_pydantic_model

from common.views import CustomView

from schools.schemas import SchoolDTO, SchoolPostParams
from schools.models import School


def SchoolCreateService(data: SchoolPostParams) -> SchoolDTO:
    try:
        school_data = get_school_pydantic_model(**data.dict()).dict()
    except Exception as e:
        return 404, "Not found."

    try:
        school = School.objects.create(**school_data)
    except IntegrityError:
        return 409, "School already exists."
    else:
        return 201, school
