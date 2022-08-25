from typing import List


from ninja import Router, Query
from ninja.pagination import paginate


# import all class from menus.schemas
from schools.models import School
from menus.models import Menu
from menus.schemas import (
    MenuDTO,
    MenuDailyListDTO,
    MenuWeeklyListDTO,
    MenuParams,
    MenuWeeklyListParams,
)
from menus.services import MenuService, MenuWeeklyListService

router = Router(tags=["menus"])


@router.get("/", response=MenuDTO)
def get_menus(request, params: MenuParams = Query(...)):
    menus = MenuService(params)
    return menus


@router.get("/weekly/", response=MenuWeeklyListDTO)
def list_menus_weekly(request, params: MenuWeeklyListParams = Query(...)):
    weekly_list_of_daily_menus = MenuWeeklyListService(params)
    return MenuWeeklyListDTO.from_menu_list(weekly_list_of_daily_menus)
