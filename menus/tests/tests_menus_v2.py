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

from ninja_jwt.tokens import AccessToken

from django.contrib.auth import get_user_model

from schools.models import School
from menus.models import Menu
from menus.types import MenuTypes
from menus.schemas import MenuDTO, MenuWeeklyListDTO

User = get_user_model()


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


class TestMenuAPI(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(1, 4):
            school = SchoolFactory(
                code=int(str(i) * 8),
                name=f"테스트{i}초등학교",
                location="서울특별시",
                address=f"서울특별시 강남구 테헤란로 415",
                type=1,
                edu_office_code="J10",
            )
            setattr(cls, f"school_{i}", school)
        user = User.objects.create_user(
            username="test",
            password="test",
        )
        token = AccessToken.for_user(user)
        setattr(cls, "Authorization", f"Bearer {str(token)}")

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
                                dishes=f"테스트{i}초등학교 {i_month}월 {i_date}일 {MenuTypes(i_type).name}",
                                calories=100,
                            )
                            setattr(cls, f"menu_{i}_{i_month}_{i_date}_{i_type}", menu)

    def test_get_menus_success(self):
        school = getattr(self, f"school_1")
        date = datetime.date(year=2022, month=3, day=7)
        for i_type in range(1, 4):
            menu = getattr(self, f"menu_1_3_7_{i_type}")
            response = self.client.get(
                f"/api/v2/menus/?school_id={school.id}&date={date}&type={i_type}",
                HTTP_AUTHORIZATION=getattr(self, "Authorization"),
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["type"], menu.type)
            self.assertEqual(response.json()["dishes"], menu.dishes)
            self.assertEqual(response.json()["calories"], menu.calories)

    def test_get_menus_no_matching_date(self):
        school = getattr(self, f"school_1")
        wrong_date = datetime.date(year=2010, month=3, day=7)
        for i_type in range(1, 4):
            menu = getattr(self, f"menu_1_3_7_{i_type}")
            response = self.client.get(
                f"/api/v2/menus/?school_id={school.id}&date={wrong_date}&type={i_type}",
                HTTP_AUTHORIZATION=getattr(self, "Authorization"),
            )
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(response.json()["detail"], "Not Found")

    def test_get_menus_no_matching_school(self):
        date = datetime.date(year=2022, month=3, day=7)
        for i_type in range(1, 4):
            menu = getattr(self, f"menu_1_3_7_{i_type}")
            response = self.client.get(
                f"/api/v2/menus/?school_id=100&date={date}&type={i_type}",
                HTTP_AUTHORIZATION=getattr(self, "Authorization"),
            )
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(response.json()["detail"], "Not Found")

    def test_response_success_with_date_specified(self):
        school = getattr(self, f"school_1")
        date = datetime.date(year=2022, month=3, day=7)
        date_str = date.strftime("%Y-%m-%d")
        response = self.client.get(
            f"/api/v2/menus/weekly/?school_id={school.id}&date={date_str}",
            HTTP_AUTHORIZATION=getattr(self, "Authorization"),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["items"]), 5)
        self.assertEqual(response.json()["items"][0]["date"], date_str)

        # use Pydantic model schema for testing response data with django model fields
        for menu in response.json()["items"][0]["menus"]:
            self.assertEqual(
                MenuDTO(**menu),
                MenuDTO(**getattr(self, f"menu_1_{3}_{7}_{menu['type']}").__dict__),
            )

    # https://stackoverflow.com/questions/1042900/django-unit-testing-with-date-time-based-objects
    @patch("utils.dates.today", return_value=datetime.date(year=2022, month=8, day=24))
    def test_response_success_this_week(self, mock_today):
        school = getattr(self, f"school_1")
        first_date = datetime.date(year=2022, month=8, day=22)
        date_str = first_date.strftime("%Y-%m-%d")
        response = self.client.get(
            f"/api/v2/menus/weekly/?school_id={school.id}",
            HTTP_AUTHORIZATION=getattr(self, "Authorization"),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["items"]), 5)
        self.assertEqual(response.json()["items"][0]["date"], date_str)

        # use Pydantic model schema for testing response data with django model fields
        for menu in response.json()["items"][0]["menus"]:
            self.assertEqual(
                MenuDTO(**menu),
                MenuDTO(**getattr(self, f"menu_1_{8}_{22}_{menu['type']}").__dict__),
            )

    def test_response_success_but_empty_menu_list(self):
        school = getattr(self, f"school_1")
        date = datetime.date(year=2022, month=2, day=7)
        date_str = date.strftime("%Y-%m-%d")
        response = self.client.get(
            f"/api/v2/menus/weekly/?school_id={school.id}&date={date_str}",
            HTTP_AUTHORIZATION=getattr(self, "Authorization"),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["items"], [])

    def test_response_fail_invalid_date_format(self):
        school = getattr(self, f"school_1")
        response = self.client.get(
            f"/api/v2/menus/weekly/?school_id={school.id}&date=22-08-24",
            HTTP_AUTHORIZATION=getattr(self, "Authorization"),
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
