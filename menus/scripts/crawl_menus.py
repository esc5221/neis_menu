from __future__ import annotations

import requests
import re

from datetime import date, datetime
from typing import List, Optional, Any
from pydantic import BaseModel, Field, validator

from neis_menu.settings import NEIS_API_KEY

from menus.types import MenuTypes
from menus.models import Menu

from schools.models import School

import pprint


# https://stackoverflow.com/questions/69306103/is-it-possible-to-change-the-output-alias-in-pydantic
# field name : Model에 저장되는 field name
# alias : input으로 받는 json field name


class MenuPydanticModel(BaseModel):
    '''
    Pydantic model corresponding to Menu Django model.
    Converts menu API response to pydantic model
    '''

    school_code: int = Field(alias='SD_SCHUL_CODE')
    school_name: str = Field(alias='SCHUL_NM')
    type: int = Field(alias='MMEAL_SC_CODE')
    date: Any = Field(alias='MLSV_YMD')
    dishes: str = Field(alias='DDISH_NM')
    calories: Any = Field(alias='CAL_INFO')

    @validator('type')
    def type_must_be_in_MenuTypes(cls, type):
        if type not in MenuTypes.values:
            raise ValueError(f'must be in {MenuTypes.values}. got {type}')
        return MenuTypes(type)

    @validator('dishes')
    def format_dishes(cls, dishes):
        regex = r'\({0,1}\d{1,2}\.\){0,1}'
        replaced = re.sub(regex, '', dishes)
        regex = r'\*{1,2}'
        replaced = re.sub(regex, '', replaced)
        regex = r'<br\/>'
        replaced = re.sub(regex, ', ', replaced)
        regex = r'\s{2,}'
        replaced = re.sub(regex, ' ', replaced)
        regex = r'\s,'
        replaced = re.sub(regex, ',', replaced)
        return replaced.strip()

    @validator('date')
    def format_date(cls, date_str):
        try:
            return datetime.strptime(date_str, '%Y%m%d')
        except:
            raise ValueError(f'date format should be %Y%m%d got {date_str}')

    @validator('calories')
    def calories_to_float(cls, calories):
        if calories is None:
            return None
        try:
            return int(float(calories.split(' ')[0]))
        except:
            print(calories.split(' ')[0])
            raise ValueError(f'calories must be int or float. got {calories}')


'''
Auto generated classes for converting json to pydantic model
'''


class RESULT(BaseModel):
    CODE: str
    MESSAGE: str


class HeadItem(BaseModel):
    list_total_count: Optional[int] = None
    RESULT: Optional[RESULT] = None


class MealServiceDietInfoItem(BaseModel):
    head: Optional[List[HeadItem]] = None
    row: Optional[List[MenuPydanticModel]] = None


class MealServiceDietInfo(BaseModel):
    mealServiceDietInfo: List[MealServiceDietInfoItem]

    class Config:
        allow_population_by_field_name = True


'''
END
'''


def get_menu(school_code, edu_office_code, start_date, end_date):
    url = f'https://open.neis.go.kr/hub/mealServiceDietInfo' \
        f'?KEY={NEIS_API_KEY}' \
        f'Type=json&' \
        f'pIndex=1&' \
        f'pSize=1000&' \
        f'&ATPT_OFCDC_SC_CODE={edu_office_code}' \
        f'&SD_SCHUL_CODE={school_code}' \
        f'&MLSV_FROM_YMD={start_date}' \
        f'&MLSV_TO_YMD={end_date}'
    response = requests.get(
        url,
        headers={'Content-Type': 'application/json'}
    )
    return response.json()


def get_menu_pydantic_model(*args):
    p = get_menu(*args)
    if p.get('mealServiceDietInfo') is None:
        return []
    m = MealServiceDietInfo(**p)
    return m.mealServiceDietInfo[1].row

# p = get_menu()
# m1 = MealServiceDietInfo(**p)
# print()

# ex)
# ./manage.py runscript crawl_menus --script-args 20220101 20220106 9300054


def run(*args):
    if args[0] == 'test':
        rs = get_menu_pydantic_model(9300054, 'I10', '20220101', '20220106')
        for i in rs:
            pprint.pprint(i.dict(), indent=2)
        return

    elif args[0] == 'prod':

        try:
            start_date = args[1]
            end_date = args[2]
            if start_date is None:
                latest_menu_date = Menu.objects.latest('date').date
                start_date = latest_menu_date + datetime.timedelta(days=1)
            if end_date is None:
                end_date = datetime.date.today()

        except Exception as e:
            print(e)
            raise Exception('start_date and end_date are in wrong format')

        else:
            count = 0
            school_infos = School.objects.values_list(
                'code', 'edu_office_code')
            for school_code, edu_office_code in school_infos:
                rs = get_menu_pydantic_model(school_code, edu_office_code,
                                             start_date, end_date)
                for i in rs:
                    valid_data_dict = i.dict()
                    valid_data_dict['school'] = School.objects.get(
                        code=school_code)
                    valid_data_dict.pop('school_code')
                    valid_data_dict.pop('school_name')
                    Menu.objects.create(**valid_data_dict)
                count += len(rs)
                print(
                    f'    * {school_code} - {len(rs)} rows  / total {count} rows are crawled')
            #rs = get_rows('9300054', 'I10', start_date, end_date)
            # for i in rs:
            #     pprint.pprint(i.dict(), indent=2)
            print(f'* total : {count} rows are crawled')
            return
