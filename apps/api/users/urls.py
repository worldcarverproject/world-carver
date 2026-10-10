from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RegisterView, ResendVerificationView, VerifyEmailView

# Create a router and register our ViewSets with it.
router = DefaultRouter()

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('verify-email/', VerifyEmailView.as_view(), name='auth_verify_email'),
    path('resend-verification/', ResendVerificationView.as_view(), name='auth_resend_verification'),
    path("", include(router.urls)),
]