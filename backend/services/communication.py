import json
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template import Context, Template
from django.utils import timezone

from campaigns.models import Campaign, CommunicationLog
from patients.models import Patient

logger = logging.getLogger(__name__)


class CommunicationService:
    @staticmethod
    def send_campaign_communication(
        campaign: Campaign, patient: Patient, custom_context=None
    ):
        """Send a campaign communication to a patient based on their preferences"""
        if not patient.can_contact():
            logger.warning(
                f"Cannot contact patient {patient.id} - preferences or consent issue"
            )
            return False

        # Determine communication method
        contact_info = patient.get_contact_info()

        # Create communication log first (for tracking)
        comm_log = CommunicationLog.objects.create(
            campaign=campaign,
            patient=patient,
            communication_type=contact_info["method"],
            status="PENDING",
            metadata={"attempt": 1},
        )

        # Track best times for communication
        current_hour = timezone.now().hour
        metadata = comm_log.metadata
        metadata["send_hour"] = current_hour
        comm_log.metadata = metadata
        comm_log.save(update_fields=["metadata"])

        # Process based on method
        if contact_info["method"] == "EMAIL":
            success = CommunicationService._send_email_campaign(
                campaign, patient, comm_log, custom_context
            )
        elif contact_info["method"] == "SMS":
            success = CommunicationService._send_sms_campaign(
                campaign, patient, comm_log, custom_context
            )
        else:
            logger.warning(f"Unsupported communication method for patient {patient.id}")
            comm_log.record_failure("Unsupported communication method")
            return False

        # Record attempt
        patient.record_contact_attempt(successful=success)
        return success

    @staticmethod
    def _send_email_campaign(campaign, patient, comm_log, custom_context=None):
        """Send an email campaign communication to a patient"""
        try:
            # Create template context with patient data
            context = {
                "username": patient.user.username,
                "first_name": getattr(patient.user, "first_name", ""),
                "email": patient.email,
                "campaign_title": campaign.title,
                # Include URLs and other template variables
                "appointment_link": f"{settings.SITE_URL}/appointment/?patient={patient.id}",
                "unsubscribe_link": f"{settings.SITE_URL}/unsubscribe/?patient={patient.id}",
                # Add current date/time for time-sensitive messages
                "current_date": timezone.now().strftime("%Y-%m-%d"),
                "current_time": timezone.now().strftime("%H:%M"),
            }

            # Add custom context if provided
            if custom_context:
                context.update(custom_context)

            # Process template
            template = Template(campaign.email_template)
            rendered_message = template.render(Context(context))

            # Convert campaign title to subject line
            subject = campaign.title

            # Send email
            send_mail(
                subject=subject,
                message="Please view this email with an HTML email client.",
                html_message=rendered_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[patient.email],
                fail_silently=False,
            )

            # Update log status
            comm_log.mark_as_sent()
            return True

        except Exception as e:
            logger.error(f"Failed to send email to patient {patient.id}: {str(e)}")
            comm_log.record_failure(str(e))
            return False

    @staticmethod
    def _send_sms_campaign(campaign, patient, comm_log, custom_context=None):
        """Send an SMS campaign communication to a patient"""
        try:
            # Create template context with patient data
            context = {
                "username": patient.user.username,
                "campaign_title": campaign.title,
                # Include URLs and other template variables
                "appointment_link": f"{settings.SITE_URL}/appointment/?p={patient.id}",
                # Add current date/time for time-sensitive messages
                "current_date": timezone.now().strftime("%Y-%m-%d"),
            }

            # Add custom context if provided
            if custom_context:
                context.update(custom_context)

            # Process template
            template = Template(campaign.sms_template)
            message = template.render(Context(context))

            # In a real implementation, you would integrate with an SMS service like Twilio
            # For now, we'll just log the message and simulate success
            logger.info(f"SMS to {patient.phone_number}: {message}")

            # Update communication log to simulate successful sending
            comm_log.mark_as_sent()
            return True

        except Exception as e:
            logger.error(f"Failed to send SMS to patient {patient.id}: {str(e)}")
            comm_log.record_failure(str(e))
            return False

    @staticmethod
    def get_optimal_send_time(patient):
        """Determine the optimal time to send a communication to this patient"""
        # Check if patient has specified preferences
        if patient.contact_time_preferences:
            try:
                preferences = patient.contact_time_preferences
                if isinstance(preferences, str):
                    preferences = json.loads(preferences)

                if preferences.get("preferred_days") and preferences.get(
                    "preferred_hours"
                ):
                    return {
                        "source": "patient_preference",
                        "preferred_days": preferences["preferred_days"],
                        "preferred_hours": preferences["preferred_hours"],
                    }
            except (json.JSONDecodeError, TypeError, KeyError):
                pass

        # If no explicit preferences, analyze past successful communications
        logs = CommunicationLog.objects.filter(
            patient=patient, status__in=["READ", "RESPONDED"]
        ).order_by("-sent_at")[:10]

        if logs.exists():
            # Count success by hour
            hour_success = {}
            for log in logs:
                if log.sent_at:
                    hour = log.sent_at.hour
                    hour_success[hour] = hour_success.get(hour, 0) + 1

            if hour_success:
                best_hour = max(hour_success.items(), key=lambda x: x[1])[0]
                return {
                    "source": "historical_analysis",
                    "preferred_hours": [best_hour, (best_hour + 1) % 24],
                    "confidence": min(
                        100, hour_success[best_hour] * 20
                    ),  # 20% per successful communication
                }

        # If no data, use general best practices
        current_hour = timezone.now().hour
        if 9 <= current_hour <= 11:  # Morning
            return {
                "source": "best_practice",
                "preferred_hours": [10, 11],
                "preferred_days": ["Monday", "Tuesday", "Wednesday", "Thursday"],
                "confidence": 60,
            }
        elif 14 <= current_hour <= 16:  # Afternoon
            return {
                "source": "best_practice",
                "preferred_hours": [14, 15],
                "preferred_days": ["Monday", "Tuesday", "Wednesday", "Thursday"],
                "confidence": 70,
            }
        else:
            return {
                "source": "best_practice",
                "preferred_hours": [10, 15],  # General business hours
                "preferred_days": ["Tuesday", "Wednesday", "Thursday"],
                "confidence": 50,
            }
