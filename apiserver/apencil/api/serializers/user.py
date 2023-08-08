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



class UserLiteSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
        ]
        read_only_fields = [
            "id",
        ]