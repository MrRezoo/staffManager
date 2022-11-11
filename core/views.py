# Create your views here.
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

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
        return redirect("search")


class UserDashboard(LoginRequiredMixin, View):
    template_name = "core/dashboard.html"
    form_class = ProfileForm

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        return render(
            request, self.template_name, {"user": user, "form": self.form_class}
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "your profile updated successfully", "info")
            return redirect("core:dashboard", request.user.username)
