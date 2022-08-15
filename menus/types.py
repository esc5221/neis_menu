from django.db import models


class MenuTypes(models.IntegerChoices):
    아침 = (1, '아침')
    점심 = (2, '점심')
    저녁 = (3, '저녁')