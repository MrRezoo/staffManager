from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from hr.models import User, NormalStaff, Salary, Profile, SalaryAdmin, HRAdmin


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "email", "staff_type")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "email",
                    "first_name",
                    "last_name",
                    "staff_type",
                ),
            },
        ),
    )

    list_display = BaseUserAdmin.list_display + ("staff_type",)
    list_filter = BaseUserAdmin.list_filter + ("staff_type",)
    search_fields = BaseUserAdmin.search_fields + ("staff_type",)


@admin.register(NormalStaff, HRAdmin, SalaryAdmin)
class EmployeeAdmin(admin.ModelAdmin):
    fields = (
        "username",
        "email",
        "first_name",
        "last_name",
        "staff_type",
        "user_permissions",
    )
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "staff_type",
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "co_email", "birth_date", "national_code")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser or request.user.staff_type == "HRA":
            return queryset
        return queryset.filter(user=request.user)


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ("name", "amount")
