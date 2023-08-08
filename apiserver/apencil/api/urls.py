from django.urls import path

# Create urls here

from apencil.api.views import (
    # Authentication
    SignUpEndpoint,
    SignInEndpoint,
)

urlpatterns = [
    # Auth
    path("sign-up/", SignUpEndpoint.as_view(), name="sign-up"),
    path("sign-in/", SignInEndpoint.as_view(), name="sign-in"),
]