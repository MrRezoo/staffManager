from django.db import models


class ModificationMixin(models.Model):
    _created_time = models.DateTimeField(auto_now_add=True, null=True)
    _modified_time = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

    @property
    def created_time(self):
        return self._created_time

    @property
    def updated_time(self):
        return self._modified_time
