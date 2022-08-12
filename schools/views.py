from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from schools.models import School
from schools.schemas import SchoolSchema

from schools.scripts.crawl_schools import get_school_pydantic_model


class SchoolView(APIView):
    model = School
    schema = SchoolSchema

    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def get_response_data(self, instance, many=False):
        return self.schema(many=many).dump(instance).data

    def get(self, request, pk):
        instance = self.get_object(pk=pk)
        return Response(SchoolSchema(**instance.__dict__).dict(), status=status.HTTP_200_OK)


class SchoolListCreateView(APIView):
    model = School
    schema = SchoolSchema

    def get_response_data(self, instance_or_queryset, many=False):
        if many == True:
            instance_list = self.model.__name__.lower() + '_list'
            response_data = {instance_list: []}
            for instance in instance_or_queryset:
                response_data[instance_list].append(
                    self.schema(**instance.__dict__).dict())
        else:
            response_data = self.schema(**instance_or_queryset.__dict__).dict()
        return response_data

    def get(self, request):
        instance = self.model.objects.all()
        return Response(self.get_response_data(instance, many=True), status=status.HTTP_200_OK)

    def post(self, request):
        school_code = request.data.get('school_code')
        try:
            school_data = get_school_pydantic_model(school_code).dict()
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            School.objects.create(**school_data)
            return Response(status=status.HTTP_201_CREATED)
