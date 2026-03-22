from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
import redis

from .models import VerificationRequest
from .serializers import VerificationRequestSerializer
from .tasks import check_request_status
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
        response = super().create(request, *args, **kwargs)

        request_id = response.data.get("id")

        check_request_status.apply_async(args=[request_id], countdown=120)

        return response

    @action(detail=True, methods=["patch"], url_path="status")
    def update_status(self, request, pk=None):
        instance = self.get_object()
        new_status = request.data.get("status")

        if new_status not in dict(VerificationRequest.StatusChoices.choices):
            return Response({"error": "Invalid status"}, status=400)

        instance.status = new_status
        instance.save()

        return Response({"status": instance.status})

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        from .models import VerificationRequest

        total = VerificationRequest.objects.count()

        by_status = (
            VerificationRequest.objects
            .values('status')
            .annotate(count=Count('id'))
        )

        last_24h = VerificationRequest.objects.filter(
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).count()

        return Response({
            "total": total,
            "by_status": {item['status']: item['count'] for item in by_status},
            "last_24h": last_24h
        })