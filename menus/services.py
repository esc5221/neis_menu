import itertools

from typing import List

from utils.dates import week_start_end_date

from schools.models import School
from menus.models import Menu
from menus.schemas import MenuDTO, MenuParams, MenuWeeklyListParams


def MenuService(params: MenuParams) -> MenuDTO:
    school = School.objects.get_or_404(id=params.school_id)
    menus = Menu.objects.get_or_404(
        school_id=school, date=params.date, type=params.type
    )
    return menus


def MenuWeeklyListService(params: MenuWeeklyListParams) -> List[List[MenuDTO]]:
    week_start_date, week_end_date = week_start_end_date(params.date)

    weekly_menu_queryset = Menu.queryset.of_school(params.school_id).date_between(
        week_start_date, week_end_date
    )

    def by_date(x):
        return x.date

    weekly_list_of_daily_menus = itertools.groupby(
        sorted(weekly_menu_queryset, key=by_date), key=by_date
    )

    return weekly_list_of_daily_menus
