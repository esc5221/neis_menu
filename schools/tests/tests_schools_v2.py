import re
import json

from unittest.mock import patch

from django.http import request
from factory.django import DjangoModelFactory
from django.db import transaction

from django.test import TestCase
from rest_framework import status

from ninja_jwt.tokens import AccessToken

from django.contrib.auth import get_user_model

from schools.models import School
from schools.types import SchoolTypes
from schools.scripts.crawl_schools import SchoolPydanticModel


User = get_user_model()


class SchoolFactory(DjangoModelFactory):
    class Meta:
        model = School

    @classmethod
    def create(cls, **kwargs):
        school = School.objects.create(**kwargs)
        return school


class TestSchoolAPI(TestCase):
    @classmethod
    def setUp(cls):
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
        user = User.objects.create_user(
            username='test',
            password='test',
        )
        token = AccessToken.for_user(user)
        setattr(cls, 'Authorization', f'Bearer {str(token)}')

    def test_get_school_success(self):
        school = getattr(self, f"school_1")
        response = self.client.get(
            f'/api/v2/schools/{school.id}/', HTTP_AUTHORIZATION=getattr(self, 'Authorization'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], school.id)
        self.assertEqual(response.json()['code'], school.code)
        self.assertEqual(response.json()['name'], school.name)
        self.assertEqual(response.json()['location'], school.location)
        self.assertEqual(response.json()['address'], school.address)
        self.assertEqual(response.json()['type'], SchoolTypes(school.type).name)
        self.assertEqual(
            response.json()['edu_office_code'], school.edu_office_code)

    def test_get_school_no_matching_school_id(self):
        response = self.client.get(
            '/api/v2/schools/100/', HTTP_AUTHORIZATION=getattr(self, 'Authorization'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_schools_success(self):
        response = self.client.get(
            f'/api/v2/schools/', HTTP_AUTHORIZATION=getattr(self, 'Authorization'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['items']), 3)
        for i in range(1, 4):
            self.assertEqual(
                response.json()['items'][i-1]['name'], getattr(self, f"school_{i}").name)
            self.assertEqual(
                response.json()['items'][i-1]['name'], getattr(self, f"school_{i}").name)
            self.assertEqual(
                response.json()['items'][i-1]['code'], getattr(self, f"school_{i}").code)
            self.assertEqual(response.json()[
                             'items'][i-1]['location'], getattr(self, f"school_{i}").location)
            self.assertEqual(response.json()[
                             'items'][i-1]['address'], getattr(self, f"school_{i}").address)
            self.assertEqual(response.json()[
                             'items'][i-1]['type'], SchoolTypes(getattr(self, f"school_{i}").type).name)
            self.assertEqual(response.json()[
                             'items'][i-1]['edu_office_code'], getattr(self, f"school_{i}").edu_office_code)

    def test_list_schools_success_but_empty_items(self):
        School.objects.all().delete()
        response = self.client.get(
            f'/api/v2/schools/', HTTP_AUTHORIZATION=getattr(self, 'Authorization'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['items']), 0)

    get_school_pydantic_model_response = {
        "ATPT_OFCDC_SC_CODE": "I10",
        "ATPT_OFCDC_SC_NM": "세종특별자치시교육청",
        "SD_SCHUL_CODE": "9300054",
        "SCHUL_NM": "세종고등학교",
        "ENG_SCHUL_NM": "Sejong High School",
        "SCHUL_KND_SC_NM": "고등학교",
        "LCTN_SC_NM": "세종특별자치시",
        "JU_ORG_NM": "세종특별자치시교육청",
        "FOND_SC_NM": "공립",
        "ORG_RDNZC": "30017 ",
        "ORG_RDNMA": "세종특별자치시  조치원읍 조치원중고길 10",
        "ORG_RDNDA": "/ 세종고등학교 (조치원읍)",
        "ORG_TELNO": "044-320-6641",
        "HMPG_ADRES": "http://sejong.sjeduhs.kr/",
        "COEDU_SC_NM": "남",
        "ORG_FAXNO": "044-320-6709",
        "HS_SC_NM": "일반고",
        "INDST_SPECL_CCCCL_EXST_YN": "N",
        "HS_GNRL_BUSNS_SC_NM": "일반계",
        "SPCLY_PURPS_HS_ORD_NM": None,
        "ENE_BFE_SEHF_SC_NM": "전기",
        "DGHT_SC_NM": "주간",
        "FOND_YMD": "19260429",
        "FOAS_MEMRD": "19260429",
        "LOAD_DTM": "20220807"
    }

    @patch("schools.views.get_school_pydantic_model", return_value=SchoolPydanticModel(**get_school_pydantic_model_response))
    def test_post_schools_response_success(self, mock_get_school_pydantic_model):
        response = self.client.post(f'/api/v2/schools/',
                                    data={'school_code': 9300054},
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION=getattr(
                                        self, 'Authorization')
                                    )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['name'], '세종고등학교')
        self.assertEqual(response.json()['code'], 9300054)
        self.assertEqual(response.json()['location'], '세종특별자치시')
        self.assertEqual(
            response.json()['address'], '세종특별자치시  조치원읍 조치원중고길 10')
        self.assertEqual(response.json()['type'], SchoolTypes(3).name)
        self.assertEqual(response.json()['edu_office_code'], 'I10')

    def test_post_schools_response_no_school_code(self):
        response = self.client.post(f'/api/v2/schools/',
                                    data={},
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION=getattr(
                                        self, 'Authorization')
                                    )

        self.assertEqual(response.status_code,
                         status.HTTP_422_UNPROCESSABLE_ENTITY)

    @patch("schools.services.get_school_pydantic_model", return_value=None)
    def test_post_schools_response_neis_api_fail(self, mock_get_school_pydantic_model):
        def IndexError():
            raise IndexError()
        mock_get_school_pydantic_model.raiseError.side_effect = IndexError
        response = self.client.post(f'/api/v2/schools/',
                                    data={'school_code': 9300054},
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION=getattr(
                                        self, 'Authorization')
                                    )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['detail'], 'Not found.')

    @patch("schools.views.get_school_pydantic_model", return_value=SchoolPydanticModel(**get_school_pydantic_model_response))
    def test_post_schools_response_duplicate_school_code(self, mock_get_school_pydantic_model):
        School.objects.create(code=9300054, name='세종고등학교', location='세종특별자치시',
                              address='세종특별자치시  조치원읍 조치원중고길 10', type=SchoolTypes(3), edu_office_code='I10')
        response = self.client.post(f'/api/v2/schools/',
                                    data={'school_code': 9300054},
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION=getattr(
                                        self, 'Authorization')
                                    )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.json()['detail'], 'School already exists.')

    @patch("schools.views.get_school_pydantic_model", return_value=SchoolPydanticModel(**get_school_pydantic_model_response))
    def test_post_schools_response_request2번연속(self, mock_get_school_pydantic_model):
        response = self.client.post(f'/api/v2/schools/',
                                    data={'school_code': 9300054},
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION=getattr(
                                        self, 'Authorization')
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['name'], '세종고등학교')
        self.assertEqual(response.json()['code'], 9300054)
        self.assertEqual(response.json()['location'], '세종특별자치시')
        self.assertEqual(
            response.json()['address'], '세종특별자치시  조치원읍 조치원중고길 10')
        self.assertEqual(response.json()['type'], SchoolTypes(3).name)
        self.assertEqual(response.json()['edu_office_code'], 'I10')

        response = self.client.post(f'/api/v2/schools/',
                                    data={'school_code': 9300054},
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION=getattr(
                                        self, 'Authorization')
                                    )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.json()['detail'], 'School already exists.')
