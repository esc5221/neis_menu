from typing import List


from django.db import models
from pydantic import BaseModel

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from common.exceptions import CustomException


class CustomView(APIView):
    model = models.Model
    schema = BaseModel

    def get_object_or_404(self, **kwargs):
        """
        Return self.model object with kwargs.
        if not found, return 404 error.
        """
        try:
            return self.model.objects.get(**kwargs)
        except self.model.DoesNotExist:
            raise CustomException(
                detail="Not found.", status_code=status.HTTP_404_NOT_FOUND
            )

    def get_response_data(self, object, many=False):
        """
        Return response data of the object(s).
        instance with many=True : List[PydanticModel] or
        many : True for many instances, False for single instance
        """
        instance_list = self.model.__name__.lower() + "_list"
        response_data = {instance_list: []}

        if many == True:
            objects = object
            # Pydantic model instance list
            if isinstance(objects, List) and len(objects) > 0:
                for object in objects:
                    response_data[instance_list].append(object.dict())
            # Django QuerySet instance
            elif isinstance(objects, models.QuerySet):
                for object in objects:
                    response_data[instance_list].append(
                        self.schema(**object.__dict__).dict()
                    )
        else:
            # Pydantic model instance
            if isinstance(object, BaseModel):
                response_data = object.dict()
            # Django Model instance
            elif isinstance(object, models.Model):
                response_data = self.schema(**object.__dict__).dict()
        return response_data

    """
    Django -> Pydantic
        PydanticModel : PydanticModel(**DjangoModel.__dict__)
        Response Dict : PydanticModel(**DjangoModel.__dict__).dict()
    Pydantic -> Django
        DjangoModel : DjangoModel(PydanticModel.dict()) 
            * The PydanticModel fields have to be the same as the DjangoModel fields.
        Response Dict : DjangoModel(PydanticModel.dict()).dict()
    """
