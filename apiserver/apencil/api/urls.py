from django.urls import path

# Create urls here

from apencil.api.views import (
    # Authentication
    SignUpEndpoint,
    SignInEndpoint,
)