import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django_celery_beat.models import IntervalSchedule, PeriodicTask

def ensure_periodic_task():
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.MINUTES
    )
    PeriodicTask.objects.get_or_create(
        interval=schedule,
        name='Check stale requests',
        task='api.tasks.check_stale_requests',
    )

if __name__ == "__main__":
    ensure_periodic_task()
    print("✅ Periodic task ensured")