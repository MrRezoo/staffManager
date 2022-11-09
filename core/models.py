from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.validators import is_valid_iran_code


class User(AbstractUser):
    class Types(models.TextChoices):
        NORMAL_STAFF = "NS", "Normal Staff"
        HR_ADMIN = "HRA", "HR Admin"
        SALARY_ADMIN = "SA", "Salary Admin"

    type = models.CharField(
        _("Types"), max_length=3, choices=Types.choices, default=Types.NORMAL_STAFF
    )

    birth_date = models.DateField(_("Birth date of User"), null=True, blank=True)
    national_code = models.IntegerField(
        _("National code of User"),
        validators=[is_valid_iran_code],
        null=True,
        blank=True,
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
