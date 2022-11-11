from rest_framework import serializers

from hr.models import Profile, User, NormalStaff


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("co_email", "birth_date", "national_code")


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ("full_name", "username", "email", "staff_type", "profile")


class CreateNormalStaff(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        return NormalStaff(email=validated_data["email"])

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        return instance
