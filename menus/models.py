from django.db import models
from django.db.models.query import QuerySet

from common.models import BaseModel, BaseModelManager
from schools.models import School

from menus.types import MenuTypes


class MenuQuerySet(QuerySet):
    def of_school(self, school_id):
        return self.filter(school_id=school_id)

    def date_between(self, start_date, end_date):
        return self.filter(date__gte=start_date, date__lte=end_date)


class Menu(BaseModel):
    queryset = MenuQuerySet.as_manager()

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    type = models.IntegerField(choices=MenuTypes.choices)
    date = models.DateField()
    dishes = models.CharField(max_length=500, blank=True, null=False)
    calories = models.PositiveIntegerField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["school", "type", "date"], name="unique_school_type_date"
            )
        ]
        indexes = [models.Index(fields=["school", "date"], name="school_date_idx")]

    def __str__(self):
        return self.school.name + " " + self.get_type_display() + " " + str(self.date)
