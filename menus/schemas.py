from typing import List, Optional, Any
from datetime import date

from pydantic import BaseModel, validator

from schools.types import SchoolTypes

class MenuSchema(BaseModel):
    type: int
    dishes: str
    calories: int


class MenuListByDateSchema(BaseModel):
    date: date
    menus: List[MenuSchema]
