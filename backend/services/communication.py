import logging

from django.conf import settings
from django.core.mail import send_mail

from campaigns.models import CommunicationLog

logger = logging.getLogger(__name__)


class CommunicationService:
    @staticmethod
    def send_campaign_communication(campaign, patient):
        """Send a campaign communication to a patient based on their preferences"""
        if not patient.can_contact():
            logger.warning(
                f"Cannot contact patient {patient.id} - preferences or consent issue"
            )
            return False

        # Determine communication method
        contact_info = patient.get_contact_info()
        if contact_info["method"] == "EMAIL":
            return CommunicationService.send_email_campaign(campaign, patient)
        elif contact_info["method"] == "SMS":
            return CommunicationService.send_sms_campaign(campaign, patient)
        else:
            logger.warning(f"Unsupported communication method for patient {patient.id}")
            return False

    @staticmethod
    def send_email_campaign(campaign, patient):
        """Send an email campaign communication to a patient"""
        try:
            # Create communication log first (for tracking)
            comm_log = CommunicationLog.objects.create(
                campaign=campaign,
                patient=patient,
                communication_type="EMAIL",
                status="PENDING",
                metadata={"attempt": 1},
            )

            # Process template with patient context
            # This is a simplified implementation - you'll want to use a proper template engine
            message = campaign.email_template.replace(
                "{patient_name}", patient.user.username
            )

            # Send email
            send_mail(
                subject=campaign.title,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[patient.email],
                fail_silently=False,
            )

            # Update log status
            comm_log.mark_as_sent()
            patient.record_contact_attempt(successful=True)
            return True

        except Exception as e:
            logger.error(f"Failed to send email to patient {patient.id}: {str(e)}")
            if "comm_log" in locals():
                comm_log.record_failure(str(e))
            patient.record_contact_attempt(successful=False)
            return False

    @staticmethod
    def send_sms_campaign(campaign, patient):
        """Send an SMS campaign communication to a patient"""
        # Similar implementation to email but using SMS provider
        # Example with Twilio would go here
        pass
