from django.db import models

# Create your models here.
class School(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=100, blank=False)
    location = models.CharField(max_length=100, blank=True, null=False)
    address = models.CharField(max_length=100, blank=True, null=False)

    class Meta:
        pass

    def __str__(self):
        return self.name

