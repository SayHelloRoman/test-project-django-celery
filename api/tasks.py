from celery import shared_task

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