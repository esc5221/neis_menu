from django.db import IntegrityError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from schools.models import School
from schools.schemas import SchoolSchema

from schools.scripts.crawl_schools import get_school_pydantic_model

from common.views import CustomView
from common.exceptions import CustomException


class SchoolView(CustomView):
    model = School
    schema = SchoolSchema

    def get(self, request, pk):
        school = self.get_object_or_404(pk=pk)
        return Response(self.get_response_data(school), status=status.HTTP_200_OK)


class SchoolListCreateView(CustomView):
    model = School
    schema = SchoolSchema

    def get(self, request):
        schools = self.model.objects.all()
        return Response(self.get_response_data(schools, many=True), status=status.HTTP_200_OK)

    def post(self, request):

        school_code = request.data.get('school_code')
        if school_code is None:
            raise CustomException(
                detail='School code is required.', status_code=status.HTTP_400_BAD_REQUEST)

        try:
            school_data = get_school_pydantic_model(school_code).dict()
        except Exception as e:
            raise CustomException(
                detail='Not found.', status_code=status.HTTP_404_NOT_FOUND)

        try:
            school = School.objects.create(**school_data)
        except IntegrityError:
            raise CustomException(
                detail='School already exists.', status_code=status.HTTP_409_CONFLICT)
        else:
            return Response(self.get_response_data(school), status=status.HTTP_201_CREATED)
