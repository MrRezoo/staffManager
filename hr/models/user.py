from django.conf import settings
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from hr.models.models_mixin import ModificationMixin
from hr.validators import is_valid_iran_code


class User(ModificationMixin, AbstractUser):
    username_validator = UnicodeUsernameValidator()

    class StaffTypes(models.TextChoices):
        NORMAL_STAFF = "NS", "Normal Staff"
        HR_ADMIN = "HRA", "HR Admin"
        SALARY_ADMIN = "SA", "Salary Admin"

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        null=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(unique=True)

    staff_type = models.CharField(
        _("Types"),
        max_length=3,
        choices=StaffTypes.choices,
        default=StaffTypes.NORMAL_STAFF,
    )

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("core:dashboard", args=[self.username])

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def permission_handler(self):
        if self.staff_type == self.StaffTypes.NORMAL_STAFF:
            self.set_normal_staff_permissions()
        if self.staff_type == self.StaffTypes.HR_ADMIN:
            self.set_hr_admin_permissions()
        if self.staff_type == self.StaffTypes.SALARY_ADMIN:
            self.set_hr_admin_permissions()

    def set_normal_staff_permissions(self):
        permissions_code_name = ["view_profile", "view_salary"]
        content_type = ContentType.objects.filter(model="normalstaff").first()
        permissions = Permission.objects.filter(
            codename__in=permissions_code_name, content_type=content_type
        )
        self.user_permissions.set(permissions)
        self.is_staff = True

    def set_hr_admin_permissions(self):
        permissions_code_name = ["view_profile", "change_profile", "view_salary"]
        content_type = ContentType.objects.filter(model="hradmin").first()
        permissions = Permission.objects.filter(
            codename__in=permissions_code_name, content_type=content_type
        )
        self.user_permissions.set(permissions)
        self.is_staff = True

    def set_salary_admin_permissions(self):
        permissions_code_name = [
            "view_profile",
            "view_salary",
            "change_salary",
            "add_salary",
        ]
        content_type = ContentType.objects.filter(model="salaryadmin").first()
        permissions = Permission.objects.filter(
            codename__in=permissions_code_name, content_type=content_type
        )
        self.user_permissions.set(permissions)
        self.is_staff = True


class Profile(ModificationMixin, models.Model):
    co_email = models.EmailField(_("Company email address"), blank=True)
    birth_date = models.DateField(_("Birth date of User"), null=True, blank=True)
    national_code = models.CharField(
        _("National code of User"),
        validators=[is_valid_iran_code],
        max_length=12,
        null=True,
        blank=True,
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.full_name} "

    def name(self):
        return self.user.full_name
