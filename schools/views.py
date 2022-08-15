from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from schools.models import School
from schools.schemas import SchoolSchema

from schools.scripts.crawl_schools import get_school_pydantic_model

from common.views import CustomView


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
        try:
            school_data = get_school_pydantic_model(school_code).dict()
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            School.objects.create(**school_data)
            return Response(status=status.HTTP_201_CREATED)
