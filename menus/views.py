import datetime
import itertools

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from menus.models import Menu
from menus.schemas import MenuSchema, MenuListOfDateSchema

from menus.scripts.crawl_menus import get_menu_pydantic_model

from common.views import CustomView
from common.exceptions import CustomException


class MenuView(CustomView):
    model = Menu
    schema = MenuSchema

    def get(self, request, school_id):
        date = request.query_params.get('date')
        type = request.query_params.get('type')

        if date is None:
            raise CustomException(detail='date is required',
                                  status_code=status.HTTP_400_BAD_REQUEST)
        if type is None:
            raise CustomException(detail='type is required',
                                  status_code=status.HTTP_400_BAD_REQUEST)

        menu = self.get_object_or_404(
            school_id=school_id,
            date=date,
            type=type
        )

        return Response(self.get_response_data(menu), status=status.HTTP_200_OK)


class MenuWeeklyView(CustomView):
    model = Menu
    schema = MenuSchema

    def get_week_start_end_date(self, date):
        week_start_date = date - datetime.timedelta(days=date.weekday())
        week_end_date = week_start_date + datetime.timedelta(days=6)

        return week_start_date, week_end_date

    def get(self, request, school_id):
        if (date := request.query_params.get('date')) is None:
            date = datetime.date.today()
        else:
            try:
                date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            except ValueError:
                raise CustomException(
                    detail='Invalid date format.', status_code=status.HTTP_400_BAD_REQUEST)

        week_start_date, week_end_date = self.get_week_start_end_date(date)

        weekly_menu_queryset = self.model.objects.filter(
            school_id=school_id,
            date__gte=week_start_date, date__lte=week_end_date
        )

        def by_date(x): return x.date

        # split Menu object(evaluated from queryset) list by date
        # https://stackoverflow.com/questions/67871570/how-to-split-a-list-into-sublists-based-on-unique-values-of-one-column
        weekly_menu_object_list_grouped_by_date = itertools.groupby(
            sorted(weekly_menu_queryset, key=by_date),
            key=by_date
        )

        weekly_menu_list = []
        # 1. Convert each date's Menu object(Django model) list(아침, 점심, 저녁) to MenuSchema(Pydantic) list
        # 2. Create MenuListOfDateSchema for each date and corresponding MenuSchema list
        # 2. Append each MenuListOfDateSchema list to weekly_menu_list
        for date, menu_object in weekly_menu_object_list_grouped_by_date:
            menu_schema_list = list(
                map(lambda obj: MenuSchema(**obj.__dict__), menu_object)
            )
            weekly_menu_list.append(
                MenuListOfDateSchema(
                    date=date,
                    menus=menu_schema_list
                )
            )

        return Response(self.get_response_data(weekly_menu_list, many=True), status=status.HTTP_200_OK)
