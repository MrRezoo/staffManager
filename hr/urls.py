from rest_framework.routers import DefaultRouter

from hr.views import UserViewSet

app_name = "hr"
router = DefaultRouter()

router.register(r"users", UserViewSet, basename="users")

urlpatterns = router.urls
