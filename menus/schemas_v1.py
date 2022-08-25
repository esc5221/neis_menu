from typing import List, Optional, Any
from datetime import date

from pydantic import BaseModel, validator

from schools.types import SchoolTypes


class MenuSchema(BaseModel):
    """
    식사별 메뉴 정보를 담고 있는 모델
    """

    type: int
    dishes: str
    calories: int


class MenuListOfDateSchema(BaseModel):
    """
    일자별 메뉴 리스트 (MenuSchema 리스트)를 담고 있는 모델
    menus는 최대 3개의 MenuSchema를 담게 된다.
    """

    date: date
    menus: List[MenuSchema]
