from django.db import models

from schools.models import School

from menus.types import MenuTypes


class Menu(models.Model):

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    # type은 파이썬 빌트인 함수라서 의도치 않은 동작이 발생할 수 있음
    type = models.IntegerField(choices=MenuTypes.choices)
    date = models.DateField()
    dishes = models.CharField(max_length=500, blank=True, null=False)
    calories = models.PositiveIntegerField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['school', 'type', 'date'], name='unique_school_type_date')
        ]
        indexes = [
            models.Index(fields=['date', 'school'], name='date_school_idx')
        ]

    def __str__(self):
        return self.school.name + ' ' + self.get_type_display() + ' ' + str(self.date)


