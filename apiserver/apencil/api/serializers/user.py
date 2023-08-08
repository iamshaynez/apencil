# Module import
from .base import BaseSerializer
from apencil.db.models import User


class UserSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "last_active",
        ]
        extra_kwargs = {"password": {"write_only": True}}

        # If the user has already filled first name or last name then he is onboarded
        def get_is_onboarded(self, obj):
            return bool(obj.first_name) or bool(obj.last_name)


class UserLiteSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "avatar",
            "is_bot",
        ]
        read_only_fields = [
            "id",
            "is_bot",
        ]