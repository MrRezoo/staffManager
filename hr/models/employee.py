from django.contrib.auth.base_user import BaseUserManager
from django.db import models

from .user import User


class NormalStaffManger(BaseUserManager, models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(staff_type=User.StaffTypes.NORMAL_STAFF)
        )


class HRAdminManger(BaseUserManager, models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(staff_type=User.StaffTypes.HR_ADMIN)
        )


class SalaryAdminManger(BaseUserManager, models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(staff_type=User.StaffTypes.SALARY_ADMIN)
        )


class NormalStaff(User):
    objects = NormalStaffManger()

    class Meta:
        proxy = True
        permissions = [
            ("view_profile", "Can view profile"),
            ("view_salary", "Can view salary"),
        ]


class HRAdmin(User):
    objects = HRAdminManger()

    class Meta:
        proxy = True
        permissions = [
            ("view_profile", "Can view profile"),
            ("change_profile", "Can change profile"),
            ("view_salary", "Can view salary"),
        ]

    def save(self, *args, **kwargs):
        if not self.pk:
            self.StaffTypes = User.StaffTypes.HR_ADMIN
        return super().save(self, *args, **kwargs)


class SalaryAdmin(User):
    objects = SalaryAdminManger()

    class Meta:
        proxy = True
        permissions = [
            ("view_profile", "Can view profile"),
            ("view_salary", "Can view salary"),
            ("change_salary", "Can change salary"),
            ("add_salary", "Can add salary"),
        ]

    def save(self, *args, **kwargs):
        if not self.pk:
            self.StaffTypes = User.StaffTypes.SALARY_ADMIN
        return super().save(self, *args, **kwargs)
