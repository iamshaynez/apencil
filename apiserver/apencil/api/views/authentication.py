# Python imports
import uuid
import random
import string
import json
import requests

# Django imports
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.conf import settings
from django.contrib.auth.hashers import make_password

# Third party imports
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from sentry_sdk import capture_exception, capture_message

# Module imports
from . import BaseAPIView
from apencil.db.models import User
from apencil.api.serializers import UserSerializer
# from plane.settings.redis import redis_instance
# from plane.bgtasks.magic_link_code_task import magic_link


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return (
        str(refresh.access_token),
        str(refresh),
    )


class SignUpEndpoint(BaseAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            if not settings.ENABLE_SIGNUP:
                return Response(
                    {
                        "error": "New account creation is disabled. Please contact your site administrator"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            email = request.data.get("email", False)
            password = request.data.get("password", False)

            ## Raise exception if any of the above are missing
            if not email or not password:
                return Response(
                    {"error": "Both email and password are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            email = email.strip().lower()

            try:
                validate_email(email)
            except ValidationError as e:
                return Response(
                    {"error": "Please provide a valid email address."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if the user already exists
            if User.objects.filter(email=email).exists():
                return Response(
                    {"error": "User with this email already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User.objects.create(email=email, username=uuid.uuid4().hex)
            user.set_password(password)

            # settings last actives for the user
            user.last_active = timezone.now()
            user.token_updated_at = timezone.now()
            user.save()

            serialized_user = UserSerializer(user).data

            access_token, refresh_token = get_tokens_for_user(user)

            data = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": serialized_user,
            }

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            capture_exception(e)
            return Response(
                {"error": "Something went wrong please try again later"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SignInEndpoint(BaseAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            email = request.data.get("email", False)
            password = request.data.get("password", False)

            ## Raise exception if any of the above are missing
            if not email or not password:
                return Response(
                    {"error": "Both email and password are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            email = email.strip().lower()

            try:
                validate_email(email)
            except ValidationError as e:
                return Response(
                    {"error": "Please provide a valid email address."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User.objects.filter(email=email).first()

            if user is None:
                return Response(
                    {
                        "error": "Sorry, we could not find a user with the provided credentials. Please try again."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Sign up Process
            if not user.check_password(password):
                return Response(
                    {
                        "error": "Sorry, we could not find a user with the provided credentials. Please try again."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            serialized_user = UserSerializer(user).data

            # settings last active for the user
            user.last_active = timezone.now()
            user.save()

            access_token, refresh_token = get_tokens_for_user(user)
            
            data = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": serialized_user,
            }

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            capture_exception(e)
            return Response(
                {
                    "error": "Something went wrong. Please try again later or contact the support team."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class SignOutEndpoint(BaseAPIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token", False)

            if not refresh_token:
                capture_message("No refresh token provided")
                return Response(
                    {
                        "error": "Something went wrong. Please try again later or contact the support team."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User.objects.get(pk=request.user.id)

            user.save()

            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "success"}, status=status.HTTP_200_OK)
        except Exception as e:
            capture_exception(e)
            return Response(
                {
                    "error": "Something went wrong. Please try again later or contact the support team."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

