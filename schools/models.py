from django.db import models

from schools.types import SchoolTypes, EduOffices

class School(models.Model):

    code = models.IntegerField(unique=True)
    edu_office_code = models.CharField(max_length=10, choices=EduOffices.choices)
    name = models.CharField(max_length=100, blank=False)
    type = models.IntegerField(choices=SchoolTypes.choices)
    location = models.CharField(max_length=100, blank=True, null=False)
    address = models.CharField(max_length=100, blank=True, null=False)

    class Meta:
        pass

    def __str__(self):
        return self.name
