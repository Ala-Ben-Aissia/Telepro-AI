import logging

from celery import shared_task
from django.utils import timezone

from patients.models import Patient, ConsentRecord

logger = logging.getLogger(__name__)


@shared_task(
    name="patients.tasks.update_all_engagement_scores",
    bind=True,
    max_retries=3,
    default_retry_delay=300,  # 5 minutes
)
def update_all_engagement_scores(self):
    """
    Update engagement scores for all patients in the database.
    This is a resource-intensive task that should be run periodically.
    """
    logger.info("Starting batch update of patient engagement scores")
    try:
        # Get all non-anonymized patients
        patients = Patient.objects.filter(is_anonymized=False)
        total = patients.count()
        updated = 0

        for patient in patients:
            try:
                patient.update_engagement_score()
                updated += 1
                if updated % 100 == 0:
                    logger.info(f"Updated {updated}/{total} patient engagement scores")
            except Exception as e:
                logger.error(f"Error updating score for patient {patient.id}: {str(e)}")

        logger.info(f"Completed engagement score updates: {updated}/{total} successful")
        return f"Updated {updated} out of {total} patient engagement scores"

    except Exception as exc:
        logger.error(f"Error in batch engagement score update: {str(exc)}")
        self.retry(exc=exc)


@shared_task(
    name="patients.tasks.process_scheduled_deletions",
    bind=True,
    max_retries=3,
    default_retry_delay=300,  # 5 minutes
)
def process_scheduled_deletions(self):
    """
    Process all patients scheduled for deletion (GDPR compliance).
    """
    logger.info("Starting scheduled deletion processing")
    try:
        # Find patients scheduled for deletion where the scheduled date has passed
        deletion_candidates = Patient.objects.filter(
            scheduled_deletion_date__isnull=False,
            scheduled_deletion_date__lte=timezone.now(),
            is_anonymized=False,
        )

        if not deletion_candidates.exists():
            logger.info("No patients scheduled for deletion at this time")
            return "No patients to delete"

        total = deletion_candidates.count()
        logger.info(f"Found {total} patients scheduled for deletion")

        processed = 0
        for patient in deletion_candidates:
            try:
                patient.anonymize()
                processed += 1
                logger.info(f"Anonymized patient {patient.id}")
            except Exception as e:
                logger.error(f"Failed to anonymize patient {patient.id}: {str(e)}")

        logger.info(
            f"Deletion processing complete: {processed}/{total} successfully anonymized"
        )
        return f"Processed {processed} out of {total} scheduled deletions"

    except Exception as exc:
        logger.error(f"Error in scheduled deletion processing: {str(exc)}")
        self.retry(exc=exc)


@shared_task(
    name="patients.tasks.anonymize_patient",
    bind=True,
    max_retries=3,
    default_retry_delay=60,  # 1 minute
)
def anonymize_patient(self, patient_id):
    """
    Anonymize a specific patient by ID (GDPR right to be forgotten).
    """
    try:
        patient = Patient.objects.get(id=patient_id)
        logger.info(f"Anonymizing patient {patient_id}")
        patient.anonymize()
        return f"Patient {patient_id} anonymized successfully"
    except Patient.DoesNotExist:
        logger.warning(f"Patient {patient_id} not found for anonymization")
        return f"Patient {patient_id} not found"
    except Exception as exc:
        logger.error(f"Error anonymizing patient {patient_id}: {str(exc)}")
        self.retry(exc=exc)


@shared_task(
    name="patients.tasks.send_verification_email",
    bind=True,
    max_retries=3,
    default_retry_delay=60,  # 1 minute
)
def send_verification_email(self, patient_id):
    """
    Send a verification email to a patient.
    """
    from django.core.mail import send_mail
    from django.conf import settings

    try:
        patient = Patient.objects.get(id=patient_id)
        if not patient.email:
            logger.warning(f"Patient {patient_id} has no email address")
            return f"Patient {patient_id} has no email address"

        token = patient.generate_verification_token()
        verification_link = f"{settings.SITE_URL}/verify-email/{token}/"

        send_mail(
            subject="Verify Your Email Address",
            message=f"Please verify your email by clicking on this link: {verification_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[patient.email],
            fail_silently=False,
        )

        logger.info(f"Verification email sent to patient {patient_id}")
        return f"Verification email sent to patient {patient_id}"
    except Patient.DoesNotExist:
        logger.warning(f"Patient {patient_id} not found for email verification")
        return f"Patient {patient_id} not found"
    except Exception as exc:
        logger.error(
            f"Error sending verification email to patient {patient_id}: {str(exc)}"
        )
        self.retry(exc=exc)


@shared_task(
    name="patients.tasks.send_sms_verification",
    bind=True,
    max_retries=3,
    default_retry_delay=60,  # 1 minute
)
def send_sms_verification(self, patient_id):
    """
    Send a verification SMS to a patient.
    """
    from django.conf import settings

    try:
        patient = Patient.objects.get(id=patient_id)
        if not patient.phone_number:
            logger.warning(f"Patient {patient_id} has no phone number")
            return f"Patient {patient_id} has no phone number"

        token = patient.generate_verification_token()
        verification_code = token[:6]  # Use first 6 characters as verification code

        # In a real implementation, you would use Twilio or another SMS service
        # For now we'll just log it
        logger.info(f"SMS verification code {verification_code} for patient {patient_id}")

        # Simulated SMS sending
        if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
            try:
                # Placeholder for Twilio integration
                # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                # message = client.messages.create(
                #    body=f"Your verification code is: {verification_code}",
                #    from_=settings.TWILIO_PHONE_NUMBER,
                #    to=patient.phone_number
                # )
                logger.info(f"Twilio would send SMS to {patient.phone_number}")
            except Exception as twilio_error:
                logger.error(f"Twilio SMS error: {str(twilio_error)}")
                raise

        return f"SMS verification sent to patient {patient_id}"
    except Patient.DoesNotExist:
        logger.warning(f"Patient {patient_id} not found for SMS verification")
        return f"Patient {patient_id} not found"
    except Exception as exc:
        logger.error(
            f"Error sending SMS verification to patient {patient_id}: {str(exc)}"
        )
        self.retry(exc=exc)


@shared_task(
    name="patients.tasks.clean_expired_consents",
    bind=True,
    max_retries=3,
    default_retry_delay=300,  # 5 minutes
)
def clean_expired_consents(self):
    """
    Mark expired consent records as inactive.
    """
    logger.info("Starting expired consent cleanup")
    try:
        # Find consent records that have expired
        now = timezone.now()
        expired_consents = ConsentRecord.objects.filter(
            is_active=True, expiry_date__isnull=False, expiry_date__lt=now
        )

        count = expired_consents.count()
        if count == 0:
            logger.info("No expired consents found")
            return "No expired consents"

        # Update all expired consents
        expired_consents.update(is_active=False)
        logger.info(f"Marked {count} consent records as expired")

        return f"Processed {count} expired consent records"
    except Exception as exc:
        logger.error(f"Error in expired consent cleanup: {str(exc)}")
        self.retry(exc=exc)
