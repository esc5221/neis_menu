import re
import json
import datetime

from unittest.mock import patch

from django.http import request
from factory.django import DjangoModelFactory
from django.db import transaction

from django.test import TestCase
from django.test import tag
from rest_framework import status

from schools.models import School
from menus.models import Menu
from menus.types import MenuTypes
from menus.schemas import MenuSchema


class SchoolFactory(DjangoModelFactory):
    class Meta:
        model = School

    @classmethod
    def create(cls, **kwargs):
        school = School.objects.create(**kwargs)
        return school


class MenuFactory(DjangoModelFactory):
    class Meta:
        model = Menu

    @classmethod
    def create(cls, **kwargs):
        menu = Menu.objects.create(**kwargs)
        return menu


class TestMenuView(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(1, 4):
            school = SchoolFactory(
                code=int(str(i)*8),
                name=f'테스트{i}초등학교',
                location='서울특별시',
                address=f'서울특별시 강남구 테헤란로 415',
                type=1,
                edu_office_code='J10',
            )
            setattr(cls, f"school_{i}", school)

        # iterate within date range
        for i in range(1, 4):
            for i_month in [3, 8]:
                for i_date in range(1, 32):
                    date = datetime.date(year=2022, month=i_month, day=i_date)

                    if date_is_in_weekday := (date.weekday() < 5):
                        for i_type in range(1, 4):
                            menu = MenuFactory(
                                school=getattr(cls, f"school_{i}"),
                                type=i_type,
                                date=date,
                                dishes=f'테스트{i}초등학교 {i_month}월 {i_date}일 {MenuTypes(i_type).name}',
                                calories=100,
                            )
                            setattr(
                                cls, f"menu_{i}_{i_month}_{i_date}_{i_type}", menu)

    def test_db_data(self):
        for i in range(1, 4):
            for i_month in [3, 8]:
                for i_date in range(1, 32):
                    date = datetime.date(year=2022, month=i_month, day=i_date)
                    if date_is_in_weekday := (date.weekday() < 5):
                        for i_type in range(1, 4):
                            menu = getattr(
                                self, f"menu_{i}_{i_month}_{i_date}_{i_type}")
                            object = Menu.objects.get(id=menu.id)
                            self.assertEqual(object.school.id, menu.school.id)
                            self.assertEqual(object.type, menu.type)
                            self.assertEqual(object.date, menu.date)
                            self.assertEqual(object.dishes, menu.dishes)
                            self.assertEqual(object.calories, menu.calories)

    # GET method 사용 시, data가 전송되지 않는 오류 해결
    # https://stackoverflow.com/questions/59919695/get-body-is-not-being-sent-with-apiclient-django-drf
    def test_response_success(self):
        for i in range(1, 4):
            for i_month in [3, 8]:
                for i_date in range(1, 32):
                    date = datetime.date(year=2022, month=i_month, day=i_date)
                    if date_is_in_weekday := (date.weekday() < 5):
                        for i_type in range(1, 4):
                            menu = getattr(
                                self, f"menu_{i}_{i_month}_{i_date}_{i_type}")
                            response = self.client.get(
                                f'/api/v1/schools/{i}/menus/?date={date}&type={i_type}')
                            self.assertEqual(
                                response.status_code, status.HTTP_200_OK)
                            self.assertEqual(response.data['type'], menu.type)
                            self.assertEqual(
                                response.data['dishes'], menu.dishes)
                            self.assertEqual(
                                response.data['calories'], menu.calories)

    def test_response_fail(self):
        for i in range(1, 2):
            for i_month in [7]:
                for i_date in range(1, 7):
                    date = datetime.date(year=2022, month=i_month, day=i_date)
                    if date_is_in_weekday := (date.weekday() < 5):
                        for i_type in range(1, 4):
                            response = self.client.get(
                                f'/api/v1/schools/{i}/menus/?date={date}&type={i_type}')
                            self.assertEqual(
                                response.status_code, status.HTTP_404_NOT_FOUND)
                            self.assertEqual(
                                response.data['detail'], 'Not found.')

    def test_response_fail_school_code(self):
        date = datetime.date(year=2022, month=3, day=7)
        for i_type in range(1, 4):
            response = self.client.get(
                f'/api/v1/schools/100/menus/?date={date}&type={i_type}')
            self.assertEqual(
                response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(
                response.data['detail'], 'Not found.')

    def test_response_no_date(self):
        date = datetime.date(year=2022, month=3, day=7)
        for i_type in range(1, 4):
            response = self.client.get(
                f'/api/v1/schools/1/menus/?type={i_type}')
            self.assertEqual(
                response.status_code, status.HTTP_400_BAD_REQUEST)


class TestMenuWeeklyView(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(1, 4):
            school = SchoolFactory(
                code=int(str(i)*8),
                name=f'테스트{i}초등학교',
                location='서울특별시',
                address=f'서울특별시 강남구 테헤란로 415',
                type=1,
                edu_office_code='J10',
            )
            setattr(cls, f"school_{i}", school)

        # iterate within date range
        for i in range(1, 4):
            for i_month in [3, 8]:
                for i_date in range(1, 32):
                    date = datetime.date(year=2022, month=i_month, day=i_date)

                    if date_is_in_weekday := (date.weekday() < 5):
                        for i_type in range(1, 4):
                            menu = MenuFactory(
                                school=getattr(cls, f"school_{i}"),
                                type=i_type,
                                date=date,
                                dishes=f'테스트{i}초등학교 {i_month}월 {i_date}일 {MenuTypes(i_type).name}',
                                calories=100,
                            )
                            setattr(
                                cls, f"menu_{i}_{i_month}_{i_date}_{i_type}", menu)

    def test_response_success_with_date_specified(self):
        for i in range(1, 4):
            school = getattr(self, f"school_{i}")
            date = datetime.date(year=2022, month=3, day=7)
            date_str = date.strftime("%Y-%m-%d")
            response = self.client.get(
                f'/api/v1/schools/{school.id}/menus/weekly/?date={date_str}')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data['menu_list']), 5)
            self.assertEqual(response.data['menu_list'][0]['date'], date)

            # use Pydantic model schema for testing response data with django model fields
            for menu in response.data['menu_list'][0]['menus']:
                self.assertEqual(
                    MenuSchema(**menu),
                    MenuSchema(
                        **getattr(self, f"menu_{i}_{3}_{7}_{menu['type']}").__dict__
                    )
                )

    # https://stackoverflow.com/questions/1042900/django-unit-testing-with-date-time-based-objects
    @patch('menus.views.MenuWeeklyView.get_today', return_value=datetime.date(year=2022, month=8, day=24))
    def test_response_success_this_week(self, mock_today):
        for i in range(1, 4):
            school = getattr(self, f"school_{i}")
            date = datetime.date(year=2022, month=8, day=24)
            date_str = date.strftime("%Y-%m-%d")
            response = self.client.get(
                f'/api/v1/schools/{school.id}/menus/weekly/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data['menu_list']), 5)

            monday = date - datetime.timedelta(days=date.weekday())
            self.assertEqual(response.data['menu_list'][0]['date'], monday)

            # use Pydantic model schema for testing response data with django model fields
            for menu in response.data['menu_list'][0]['menus']:
                self.assertEqual(
                    MenuSchema(**menu),
                    MenuSchema(
                        **getattr(self, f"menu_{i}_{8}_{22}_{menu['type']}").__dict__
                    )
                )

    def test_response_success_but_empty_menu_list(self):
        for i in range(1, 4):
            school = getattr(self, f"school_{i}")
            date = datetime.date(year=2022, month=2, day=7)
            date_str = date.strftime("%Y-%m-%d")
            response = self.client.get(
                f'/api/v1/schools/{school.id}/menus/weekly/?date={date_str}')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['menu_list'], [])

    def test_response_fail_invalid_date_format(self):
        for i in range(1, 4):
            response = self.client.get(
                f'/api/v1/schools/{i}/menus/weekly/?date=22-08-24')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data['detail'], 'Invalid date format.')

    