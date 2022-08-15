import datetime
import itertools

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from menus.models import Menu
from menus.schemas import MenuSchema, MenuListByDateSchema

from menus.scripts.crawl_menus import get_menu_pydantic_model

from common.views import CustomView


class MenuView(CustomView):
    model = Menu
    schema = MenuSchema

    def get(self, request, school_id):
        date = request.data.get('date')
        type = request.data.get('type')

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
                return Response(status=status.HTTP_400_BAD_REQUEST)

        week_start_date, week_end_date = self.get_week_start_end_date(date)

        queryset = self.model.objects.filter(
            school_id=school_id,
            date__gte=week_start_date, date__lte=week_end_date
        )

        # https://stackoverflow.com/questions/67871570/how-to-split-a-list-into-sublists-based-on-unique-values-of-one-column
        def order_by_date(x): return x.date

        instance_list_grouped_by_date = itertools.groupby(
            sorted(queryset, key=order_by_date),
            key=order_by_date
        )

        menu_list = []
        # convert each date's Menu instance list to a MenuListByDateSchema
        # and append each MenuListByDateSchema list to menu_list
        for date, instance in instance_list_grouped_by_date:
            menu_list.append(
                MenuListByDateSchema(
                    date=date,
                    menus=list(map(lambda instance: MenuSchema(**instance.__dict__), instance)))
            )

        return Response(self.get_response_data(menu_list, many=True), status=status.HTTP_200_OK)
