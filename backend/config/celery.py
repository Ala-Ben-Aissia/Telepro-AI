import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Create the Celery app
app = Celery("telepro_ai")

# Configure Celery using Django settings
# namespace='CELERY' means all celery-related configuration keys
# should have a `CELERY_` prefix in Django settings.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load tasks from all registered Django app configs
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Configure default broker URL with fallback
app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")

# Configure Celery beat for scheduled tasks
app.conf.beat_schedule = {
    "update-engagement-scores-daily": {
        "task": "patients.tasks.update_all_engagement_scores",
        "schedule": 86400.0,  # Daily (in seconds)
    },
    "process-scheduled-deletions": {
        "task": "patients.tasks.process_scheduled_deletions",
        "schedule": 86400.0,  # Daily (in seconds)
    },
    "retrain-ml-models-weekly": {
        "task": "services.ai.tasks.retrain_patient_response_model",
        "schedule": 604800.0,  # Weekly (in seconds)
        "kwargs": {"tune_hyperparameters": True, "use_smote": True},
    },
}

# Configure additional Celery settings
app.conf.update(
    result_expires=3600,  # Results expire after 1 hour
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone=settings.TIME_ZONE,
    enable_utc=True,
    worker_prefetch_multiplier=1,  # Disable prefetching for better task distribution
    task_acks_late=True,  # Tasks are acknowledged after execution
)

# Define error handling
@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")