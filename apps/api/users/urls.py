from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RegisterView

# Create a router and register our ViewSets with it.
router = DefaultRouter()

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path("", include(router.urls)),
]