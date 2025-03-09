import logging

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Patient

logger = logging.getLogger(__name__)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_patient_profile(sender, instance, created, **kwargs):
    """
    Signal handler to automatically create a Patient profile when
    a User with user_type='PATIENT' is created.
    """
    if created and instance.user_type == "PATIENT":
        try:
            # Create the patient profile
            Patient.objects.create(
                user=instance,
                email=instance.email,  # Copy email from user
                # Don't set medical_record_number or other fields here
                # as they should be entered during onboarding
            )
            logger.info(
                f"Created patient profile for user {instance.username} (ID: {instance.id})"
            )
        except Exception as e:
            logger.error(
                f"Failed to create patient profile for user {instance.id}: {str(e)}"
            )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_patient_email(sender, instance, created, **kwargs):
    """
    Keep the patient's email in sync with the user's email.
    This ensures email changes in the user model propagate to the patient model.
    """
    if not created and instance.user_type == "PATIENT":
        try:
            if hasattr(instance, "patient_profile"):
                patient = instance.patient_profile
                if patient.email != instance.email:
                    patient.email = instance.email
                    # Don't set email_verified to False here as verification
                    # status should be managed separately
                    patient.save(update_fields=["email", "updated_at"])
                    logger.info(f"Updated email for patient {patient.id}")
        except Exception as e:
            logger.error(
                f"Failed to update patient email for user {instance.id}: {str(e)}"
            )
