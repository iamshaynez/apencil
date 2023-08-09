from django.urls import path

# Create urls here

from apencil.api.views import (
    # Authentication
    SignUpEndpoint,
    SignInEndpoint,
    BookViewSet,
)

urlpatterns = [
    # Auth
    path("sign-up/", SignUpEndpoint.as_view(), name="sign-up"),
    path("sign-in/", SignInEndpoint.as_view(), name="sign-in"),
    # Book
    path("books/", BookViewSet.as_view({"get": "list", "post": "create",}), name="book"),
    path(
        "books/<str:name>/",
        BookViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="book",
    ),
]