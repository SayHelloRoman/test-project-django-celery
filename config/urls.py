from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import VerificationRequestViewSet

router = DefaultRouter()
router.register(r"requests", VerificationRequestViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]