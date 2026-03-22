from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from .models import VerificationRequest
from .services import send_telegram_message

@shared_task
def check_request_status(request_id):
    try:
        request = VerificationRequest.objects.get(id=request_id)
    except VerificationRequest.DoesNotExist:
        return

    if request.status == "new":
        message = f"Заявка #{request.id} все еще NEW\nТелефон: {request.phone}\nАдрес: {request.address}"
        send_telegram_message(message)

@shared_task
def check_stale_requests():
    one_hour_ago = timezone.now() - timedelta(hours=1)

    requests = VerificationRequest.objects.filter(
        status='in_progress',
        updated_at__lt=one_hour_ago
    )

    for req in requests:
        send_telegram_message(f"Заявка #{req.id} зависла (in_progress > 1 часа)")