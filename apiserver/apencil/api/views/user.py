# Third party imports
from rest_framework.response import Response
from rest_framework import status
from sentry_sdk import capture_exception

# Module imports
from apencil.api.serializers import (
    UserSerializer,
)

from apencil.api.views.base import BaseViewSet, BaseAPIView

from apencil.db.models import (
    User,
)

from apencil.utils.paginator import BasePaginator

class UserEndpoint(BaseViewSet):
    serializer_class = UserSerializer
    model = User

    def get_object(self):
        return self.request.user

    def retrieve(self, request):
        try:
            serialized_data = UserSerializer(request.user).data
            return Response(
                serialized_data,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            capture_exception(e)
            return Response(
                {"error": "Something went wrong please try again later"},
                status=status.HTTP_400_BAD_REQUEST,
            )