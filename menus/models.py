from django.db import models

from schools.models import School

# Create your models here.


class Menu(models.Model):

    class MenuType(models.IntegerChoices):
        BREAKFAST = (1, '아침')
        LUNCH = (2, '점심')
        DINNER = (3, '저녁')

    school = models.ForeignKey('schools.School', on_delete=models.CASCADE)
    type = models.IntegerField(choices=MenuType.choices)
    date = models.DateField()

    def __str__(self):
        return self.school.name + ' ' + self.get_type_display() + ' ' + self.date
