# views.py

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import VerificationRequest
from .serializers import VerificationRequestSerializer
from django.conf import settings


class VerificationRequestViewSet(viewsets.ModelViewSet):
    queryset = VerificationRequest.objects.all().order_by("-created_at")
    serializer_class = VerificationRequestSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        status_param = self.request.query_params.get("status")
        source_param = self.request.query_params.get("source")

        if status_param:
            queryset = queryset.filter(status=status_param)

        if source_param:
            queryset = queryset.filter(source=source_param)

        return queryset

    def create(self, request, *args, **kwargs):
        phone = request.data.get("phone")
        address = request.data.get("address")

        redis_key = f"dup:{phone}:{address}"

        if settings.REDIS_CLIENT.exists(redis_key):
            return Response(
                {"detail": "Duplicate request within 10 minutes"},
                status=409
            )

        settings.REDIS_CLIENT.set(redis_key, "1", ex=600)

        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=["patch"], url_path="status")
    def update_status(self, request, pk=None):
        instance = self.get_object()
        new_status = request.data.get("status")

        if new_status not in dict(VerificationRequest.StatusChoices.choices):
            return Response({"error": "Invalid status"}, status=400)

        instance.status = new_status
        instance.save()

        return Response({"status": instance.status})