from django.urls import path
from django.views.generic import TemplateView

from core import views

app_name = "core"

urlpatterns = [
    path("", TemplateView.as_view(template_name="core/main.html"), name="home"),
    path("register/", views.UserRegister.as_view(), name="register"),
    path("login/", views.UserLogin.as_view(), name="login"),
    path("logout/", views.UserLogout.as_view(), name="logout"),
    path("dashboard/<str:username>/", views.UserDashboard.as_view(), name="dashboard"),
]
