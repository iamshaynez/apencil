# Python imports
import jwt
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from uuid import uuid4

# Django imports
from django.db import IntegrityError
from django.db.models import Prefetch
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import (
    Prefetch,
    OuterRef,
    Func,
    F,
    Q,
    Count,
    Case,
    Value,
    CharField,
    When,
    Max,
    IntegerField,
)
from django.db.models.functions import ExtractWeek, Cast, ExtractDay
from django.db.models.fields import DateField
from django.contrib.auth.hashers import make_password

# Third party modules
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from sentry_sdk import capture_exception

# Module imports
from apencil.api.serializers import (
    BookSerializer,
    BookLiteSerializer,
    UserLiteSerializer,
    UserSerializer,
)

from apencil.api.views.base import BaseAPIView
from . import BaseViewSet

from apencil.db.models import (
    User,
    Book,
)


class BookViewSet(BaseViewSet):
    model = Book
    serializer_class = BookSerializer

    filterset_fields = [
        "owner",
    ]

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset().select_related("owner"))
            .order_by("name")
        )

    def create(self, request):
        try:
            serializer = BookSerializer(data=request.data)
            name = request.data.get("name", False)
            desc = request.data.get("desc", False)

            if not name:
                return Response(
                    {"error": "Book name is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if len(name) > 80 or len(desc) > 200 :
                return Response(
                    {"error": "The maximum length for name is 80 and for desc is 200"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            if serializer.is_valid():
                serializer.save(owner=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(
                [serializer.errors[error][0] for error in serializer.errors],
                status=status.HTTP_400_BAD_REQUEST,
            )
        except IntegrityError as e:
            return Response(
                {"name": "You already have a book with this name"},
                status=status.HTTP_410_GONE,
            )
        except Exception as e:
            capture_exception(e)
            return Response(
                {
                    "error": "Something went wrong please try again later",
                    "identifier": None,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )