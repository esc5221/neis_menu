from django.db import models
from django.http import Http404


class BaseModelManager(models.Manager):
    def get_or_404(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            raise Http404(self.model.__name__)


class BaseModel(models.Model):
    objects = BaseModelManager()

    class Meta:
        abstract = True
