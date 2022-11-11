from django.conf import settings
from django.db import models

from hr.models.models_mixin import ModificationMixin


class Salary(ModificationMixin, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.user.full_name} | {self.amount}"

    @property
    def name(self):
        return self.user.full_name
