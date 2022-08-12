from __future__ import annotations
import requests


from typing import List, Optional, Any
from pydantic import BaseModel, Field, validator

from neis_menu.settings import NEIS_API_KEY

from schools.types import SchoolTypes, EduOffices


class SchoolPydanticModel(BaseModel):
    '''
    Pydantic model corresponding to School Django model.
    Converts school APi response to pydantic model
    '''
    
    code: int = Field(alias='SD_SCHUL_CODE')
    name: str = Field(alias='SCHUL_NM')
    edu_office_code: Any = Field(alias='ATPT_OFCDC_SC_CODE')
    type: Any = Field(alias='SCHUL_KND_SC_NM')
    location: str = Field(alias='LCTN_SC_NM')
    address: str = Field(alias='ORG_RDNMA')

    @validator('edu_office_code')
    def edu_office_code_must_be_in_EduOffices(cls, edu_office_code):
        if edu_office_code not in EduOffices.values:
            raise ValueError(
                f'must be in {EduOffices.values}. got {edu_office_code}')
        return EduOffices(edu_office_code)

    @validator('type')
    def type_must_be_in_SchoolTypes(cls, type):
        if type not in SchoolTypes.labels:
            raise ValueError(f'must be in {SchoolTypes.labels}. got {type}')
        return SchoolTypes[type]


'''
Auto generated classes for converting json to pydantic model
'''


class RESULT(BaseModel):
    CODE: str
    MESSAGE: str


class HeadItem(BaseModel):
    list_total_count: Optional[int] = None
    RESULT: Optional[RESULT] = None


class SchoolInfoItem(BaseModel):
    head: Optional[List[HeadItem]] = None
    row: Optional[List[SchoolPydanticModel]] = None


class SchoolInfo(BaseModel):
    schoolInfo: List[SchoolInfoItem]


'''
END
'''


def get_school(school_code: int):
    url = f'https://open.neis.go.kr/hub/schoolInfo' \
          f'?KEY={NEIS_API_KEY}&' \
          f'Type=json&' \
          f'pIndex=1&' \
          f'pSize=1000&' \
          f'SD_SCHUL_CODE={school_code}'
    response = requests.get(url)
    return response.json()


def get_school_pydantic_model(school_code: int):
    p = get_school(school_code)
    m = SchoolInfo(**p)
    return m.schoolInfo[1].row[0]
