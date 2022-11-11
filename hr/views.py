from rest_framework import mixins
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import GenericViewSet

from hr.models import User
from hr.serializers import UserSerializer, CreateNormalStaff


class UserViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    http_method_names = ["get", "post"]
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ("username",)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateNormalStaff
        return UserSerializer
