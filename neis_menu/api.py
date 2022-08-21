import itertools
from typing import List

from ninja import NinjaAPI, Query, Field, Schema, ModelSchema
from ninja.pagination import paginate

from django.db.models import F, Count

from schools.models import School
from menus.models import Menu

api = NinjaAPI(
    title="neis_menu API v2",
    version="2.0.0",
)




'''
================================================================================
School View Refactored
================================================================================
'''


class SchoolDTO(Schema):
    id: int
    code: int
    name: str
    location: str

class SchoolListDTO(Schema):
    objects: List[SchoolDTO]



'''
'''


@api.get("/schools/{id}/", response=SchoolDTO)
def get_school(request, id: int):
    return School.objects.get_or_404(id=id)

#@paginate

@api.get("/schools/", response=SchoolListDTO)
def list_schools(request):
    schools = School.objects.all()
    return SchoolListDTO(objects=list(schools))


'''
================================================================================
Menu View Refactored
================================================================================
'''


class MenuDTO(ModelSchema):
    class Config:
        model = Menu
        model_fields = ['type', 'dishes', 'calories']


class MenuDailyListDTO(Schema):
    date: str
    menus: List[MenuDTO]


class MenuWeeklyListDTO(Schema):
    weekly_menus: List[MenuDailyListDTO]

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
        return cls(weekly_menus=weekly_menu_list)


class GetMenuParams(Schema):
    school_id: int
    date: str
    type: int


'''
'''


@api.get("/menus/", response=MenuDTO)
def get_menus(request, params: GetMenuParams = Query(...)):

    # service로 분리.
    school = School.objects.get_or_404(id=params.school_id)
    menus = Menu.objects.get_or_404(
        school=school, date=params.date, type=params.type)
    ##

    return menus


# list 위쪽 schema를 하나 더 만든다 (과제1 같이)
@api.get("/menus/weekly/", response=List[MenuDailyListDTO])
def list_menus_weekly(request, school_id: int, date: str = None):
    #
    weekly_menu_queryset = Menu.objects.filter(
        school_id=school_id,
        date__gte='2022-04-10', date__lte='2022-04-17'
    )

    def by_date(x): return x.date

    weekly_list_of_daily_menus = itertools.groupby(
        sorted(weekly_menu_queryset, key=by_date),
        key=by_date
    )
# service로 데이터 조각을 모음.

# -> 데이터 조합하는걸 builder로 만드는 사람 있음
# -> schema에서 data조각을 합친다.

# 이를 조합해서 response형태로 return.
    weekly_menu_list = []
    for date, daily_menus in weekly_list_of_daily_menus:
        menu_schema_list = [MenuDTO.from_orm(menu) for menu in daily_menus]
        weekly_menu_list.append(
            MenuDailyListDTO(
                date=str(date),
                menus=menu_schema_list
            )
        )

    return weekly_menu_list


# list 위쪽 schema를 하나 더 만든다 (과제1 같이)
@api.get("/menus/weekly2/", response=MenuWeeklyListDTO)
def list_menus_weekly2(request, school_id: int, date: str = None):
    # service로 분리.
    weekly_menu_queryset = Menu.objects.filter(
        school_id=school_id,
        date__gte='2022-04-10', date__lte='2022-04-17'
    )

    def by_date(x): return x.date
    weekly_list_of_daily_menus = itertools.groupby(
        sorted(weekly_menu_queryset, key=by_date),
        key=by_date
    )
# service로 데이터 조각을 모음.

# -> 데이터 조합하는걸 builder로 만드는 사람 있음
# -> schema에서 data조각을 합친다.

# 이를 조합해서 response형태로 return.

    return MenuWeeklyListDTO.from_menu_list(weekly_list_of_daily_menus)

