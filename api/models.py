# models.py

from django.db import models

class VerificationRequest(models.Model):

    class SourceChoices(models.TextChoices):
        OLX = "olx"
        TELEGRAM = "telegram"
        MANUAL = "manual"

    class StatusChoices(models.TextChoices):
        NEW = "new"
        IN_PROGRESS = "in_progress"
        VERIFIED = "verified"
        REJECTED = "rejected"

    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)

    source = models.CharField(max_length=20, choices=SourceChoices.choices)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.NEW)

    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)