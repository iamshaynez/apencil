# Third party imports
from rest_framework import serializers

# Module imports
from .base import BaseSerializer
from .user import UserLiteSerializer

from apencil.db.models import (
    User,
    Book,
)

class BookSerializer(BaseSerializer):
    owner = UserLiteSerializer(read_only=True)

    class Meta:
        model = Book
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
            "owner",
        ]

class BookLiteSerializer(BaseSerializer):
    class Meta:
        model = Book
        fields = [
            "name",
            "desc",
            "id",
        ]
        read_only_fields = fields