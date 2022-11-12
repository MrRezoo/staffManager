# Create your views here.
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView

from core.forms import UserRegistrationForm, UserLoginForm, ProfileForm

User = get_user_model()


class UserRegister(View):
    form_class = UserRegistrationForm
    template_name = "core/register.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            User.objects.create_user(data["username"], data["email"], data["password"])
            messages.success(request, "you registered successfully", "info")
            return redirect("core:home")
        return render(request, self.template_name, {"form": form})


class UserLogin(View):
    template_name = "core/login.html"
    form_class = UserLoginForm

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data["username"], password=data["password"]
            )
            if user is not None:
                login(request, user)
                messages.success(request, "you are logged in successfully", "info")
                return redirect("core:home")
            messages.error(request, "username or password is wrong", "warning")
        return render(request, self.template_name, {"form": form})


class UserLogout(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        logout(request)
        messages.success(request, "you logged out successfully")
        return redirect("core:home")


class UserProfile(LoginRequiredMixin, View):
    template_name = "core/profile.html"
    form_class = ProfileForm

    def get(self, request, username):
        if request.user.staff_type == "HRA":
            user = get_object_or_404(User, username=username)
        else:
            if request.user.username != username:
                raise PermissionDenied
            user = get_object_or_404(User, username=request.user.username)
        return render(
            request, self.template_name, {"user": user, "form": self.form_class}
        )

    @method_decorator(permission_required("hr.change_profile", raise_exception=True))
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, **kwargs)
        form = self.form_class(request.POST, instance=user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "your profile updated successfully", "info")
            return redirect("core:profile", user.username)


@method_decorator(
    permission_required(["hr.view_profile", "hr.change_profile"], raise_exception=True),
    name="get",
)
class UserListView(ListView):
    model = User
    queryset = User.objects.select_related("profile").all()
    template_name = "core/users.html"
    context_object_name = "user_list"
    ordering = ("id",)
