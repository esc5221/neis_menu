from typing import List
import itertools


from ninja import Router, Query
from ninja.pagination import paginate


# import all class from menus.schemas
from menus.schemas import MenuDTO, MenuDailyListDTO, MenuWeeklyListDTO, MenuGetParams
from schools.models import School
from menus.models import Menu

router = Router(tags=["menus"])


@router.get("/", response=MenuDTO)
def get_menus(request, params: MenuGetParams = Query(...)):

    # service로 분리.
    school = School.objects.get_or_404(id=params.school_id)
    menus = Menu.objects.get_or_404(
        school=school, date=params.date, type=params.type)
    ##

    return menus


@router.get("/weekly/", response=MenuWeeklyListDTO)
def list_menus_weekly(request, school_id: int, date: str = None):
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

    return MenuWeeklyListDTO.from_menu_list(weekly_list_of_daily_menus)
