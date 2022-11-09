from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class NormalStaffManger(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super().get_queryset(*args, **kwargs).filter(type=User.Types.NORMAL_STAFF)
        )


class HRAdminManger(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.HR_ADMIN)


class SalaryAdminManger(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super().get_queryset(*args, **kwargs).filter(type=User.Types.SALARY_ADMIN)
        )


class NormalStaff(User):
    objects = NormalStaffManger()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.NORMAL_STAFF
        return super().save(self, *args, **kwargs)


class HRAdmin(User):
    objects = HRAdminManger()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.HR_ADMIN
        return super().save(self, *args, **kwargs)


class SalaryAdmin(User):
    objects = SalaryAdminManger()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.SALARY_ADMIN
        return super().save(self, *args, **kwargs)
