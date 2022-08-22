from datetime import datetime
from typing import List

from pydantic import validator
from ninja import Schema, ModelSchema

from menus.models import Menu


class MenuDTO(ModelSchema):
    class Config:
        model = Menu
        model_fields = ['type', 'dishes', 'calories']


class MenuDailyListDTO(Schema):
    date: str
    menus: List[MenuDTO]


class MenuWeeklyListDTO(Schema):
    items: List[MenuDailyListDTO]

    @classmethod
    def from_menu_list(
        cls,
        weekly_list_of_daily_menus: List[List[ModelSchema]]
    ) -> 'MenuWeeklyListDTO':
        weekly_menu_list = []
        for date, daily_menus in weekly_list_of_daily_menus:
            menu_schema_list = [MenuDTO.from_orm(menu)
                                for menu in daily_menus]
            weekly_menu_list.append(
                MenuDailyListDTO(
                    date=str(date),
                    menus=menu_schema_list
                )
            )
        return cls(items=weekly_menu_list)


class MenuParams(Schema):
    school_id: int
    date: str
    type: int

    @validator('date')
    def validate_date(cls, date_str):
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except Exception as e:
            raise ValueError(f'date format should be %Y-%m-%d got {date_str}')

class MenuWeeklyListParams(Schema):
    school_id: int
    date: str = None

    @validator('date')
    def validate_date(cls, date_str):
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except Exception as e:
            raise ValueError(f'date format should be %Y-%m-%d got {date_str}')


