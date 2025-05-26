import logging
import json
from datetime import timedelta

from celery import shared_task
from django.db.models import Q
from django.utils import timezone

from campaigns.models import Campaign, CommunicationLog, PatientSegment
from patients.models import Patient
from services.communication import CommunicationService

logger = logging.getLogger(__name__)


@shared_task(
    name="campaigns.tasks.send_campaign_communication",
    bind=True,
    max_retries=3,
    default_retry_delay=60,  # 1 minute
)
def send_campaign_communication(self, campaign_id, patient_id, custom_context=None):
    """
    Send a campaign communication to a specific patient.
    This is an asynchronous task to prevent web requests from waiting for communications to complete.

    Args:
        campaign_id: ID of the campaign
        patient_id: ID of the patient
        custom_context: Optional custom context for the communication template
    """
    try:
        from campaigns.models import Campaign
        from patients.models import Patient

        # Retrieve objects
        campaign = Campaign.objects.get(id=campaign_id)
        patient = Patient.objects.get(id=patient_id)

        # Send the communication
        logger.info(f"Sending {campaign.title} to patient {patient_id}")
        result = CommunicationService.send_campaign_communication(
            campaign=campaign, patient=patient, custom_context=custom_context
        )

        if result:
            logger.info(
                f"Successfully sent campaign {campaign_id} to patient {patient_id}"
            )
            return f"Sent campaign {campaign_id} to patient {patient_id}"
        else:
            logger.warning(
                f"Failed to send campaign {campaign_id} to patient {patient_id}"
            )
            raise Exception("Communication service failed to send message")

    except Campaign.DoesNotExist:
        logger.error(f"Campaign {campaign_id} not found")
        return f"Campaign {campaign_id} not found"
    except Patient.DoesNotExist:
        logger.error(f"Patient {patient_id} not found")
        return f"Patient {patient_id} not found"
    except Exception as exc:
        logger.error(f"Error sending campaign communication: {str(exc)}")
        self.retry(exc=exc)


@shared_task(
    name="campaigns.tasks.send_bulk_campaign",
    bind=True,
    max_retries=3,
    default_retry_delay=300,  # 5 minutes
)
def send_bulk_campaign(self, campaign_id, segment_id=None, batch_size=100):
    """
    Send a campaign to multiple patients, either based on a segment or all active patients.

    Args:
        campaign_id: ID of the campaign
        segment_id: Optional segment ID to filter patients
        batch_size: Number of communications to process in each batch
    """
    try:
        campaign = Campaign.objects.get(id=campaign_id)

        # Get patients based on segment or all active
        if segment_id:
            segment = PatientSegment.objects.get(id=segment_id)
            patient_queryset = Patient.objects.filter(is_anonymized=False)
            # Apply segment criteria (assuming criteria is a JSON with filter conditions)
            criteria = segment.criteria
            if isinstance(criteria, str):
                criteria = json.loads(criteria)

            # Apply dynamic filters based on segment criteria
            # This is a simplified version - in production you'd have more sophisticated logic
            for field, value in criteria.items():
                if field and value:
                    filter_kwargs = {field: value}
                    patient_queryset = patient_queryset.filter(**filter_kwargs)
        else:
            # Get all active patients
            patient_queryset = Patient.objects.filter(
                is_anonymized=False, email_verified=True
            )

        # Count total patients
        total_patients = patient_queryset.count()
        if total_patients == 0:
            logger.warning(f"No patients found for campaign {campaign_id}")
            return "No patients match the criteria"

        logger.info(f"Starting bulk campaign {campaign_id} to {total_patients} patients")

        # Process in batches to avoid memory issues
        processed = 0
        for i in range(0, total_patients, batch_size):
            batch = patient_queryset[i : i + batch_size]
            for patient in batch:
                # Schedule individual tasks for each patient
                send_campaign_communication.delay(
                    campaign_id=campaign_id, patient_id=patient.id
                )
                processed += 1

            logger.info(
                f"Scheduled {processed}/{total_patients} communications for campaign {campaign_id}"
            )

        return f"Scheduled bulk campaign {campaign_id} to {total_patients} patients"

    except Campaign.DoesNotExist:
        logger.error(f"Campaign {campaign_id} not found")
        return f"Campaign {campaign_id} not found"
    except PatientSegment.DoesNotExist:
        logger.error(f"Segment {segment_id} not found")
        return f"Segment {segment_id} not found"
    except Exception as exc:
        logger.error(f"Error in bulk campaign: {str(exc)}")
        self.retry(exc=exc)


@shared_task(
    name="campaigns.tasks.analyze_campaign_performance",
    bind=True,
    max_retries=3,
    default_retry_delay=300,  # 5 minutes
)
def analyze_campaign_performance(self, campaign_id):
    """
    Analyze the performance of a campaign and store metrics.

    Args:
        campaign_id: ID of the campaign to analyze
    """
    try:
        campaign = Campaign.objects.get(id=campaign_id)

        # Get all communication logs for this campaign
        logs = CommunicationLog.objects.filter(campaign_id=campaign_id)

        # Perform analysis
        total_sent = logs.filter(
            status__in=["SENT", "DELIVERED", "READ", "RESPONDED"]
        ).count()
        total_delivered = logs.filter(
            status__in=["DELIVERED", "READ", "RESPONDED"]
        ).count()
        total_read = logs.filter(status__in=["READ", "RESPONDED"]).count()
        total_responded = logs.filter(status="RESPONDED").count()

        # Calculate rates
        delivery_rate = (total_delivered / total_sent * 100) if total_sent > 0 else 0
        open_rate = (total_read / total_delivered * 100) if total_delivered > 0 else 0
        response_rate = (total_responded / total_read * 100) if total_read > 0 else 0

        # Store analytics as campaign metadata
        metadata = campaign.metadata if hasattr(campaign, "metadata") else {}

        # Update with new analytics
        analytics = {
            "analyzed_at": timezone.now().isoformat(),
            "total_sent": total_sent,
            "total_delivered": total_delivered,
            "total_read": total_read,
            "total_responded": total_responded,
            "delivery_rate": round(delivery_rate, 2),
            "open_rate": round(open_rate, 2),
            "response_rate": round(response_rate, 2),
        }

        # Add time-based analysis
        time_analysis = {}
        for hour in range(24):
            # Count successful communications by hour
            hour_responses = logs.filter(status="RESPONDED", sent_at__hour=hour).count()
            time_analysis[f"{hour:02d}:00"] = hour_responses

        analytics["time_analysis"] = time_analysis

        # Store analytics in campaign metadata
        if not hasattr(campaign, "metadata"):
            # If metadata field doesn't exist, we would need to add it to the model
            logger.warning(
                "Campaign model doesn't have metadata field, can't store analytics"
            )
        else:
            metadata["analytics"] = analytics
            campaign.metadata = metadata
            campaign.save(update_fields=["metadata"])

        logger.info(
            f"Analyzed campaign {campaign_id}: {delivery_rate:.1f}% delivery, {response_rate:.1f}% response"
        )
        return f"Analyzed campaign {campaign_id}"

    except Campaign.DoesNotExist:
        logger.error(f"Campaign {campaign_id} not found")
        return f"Campaign {campaign_id} not found"
    except Exception as exc:
        logger.error(f"Error analyzing campaign: {str(exc)}")
        self.retry(exc=exc)


@shared_task(
    name="campaigns.tasks.find_optimal_send_times",
    bind=True,
    max_retries=3,
    default_retry_delay=300,  # 5 minutes
)
def find_optimal_send_times(self):
    """
    Analyze communication logs to find optimal sending times overall.
    This task helps optimize when campaigns should be scheduled.
    """
    try:
        # Get all communications that were responded to
        successful_comms = CommunicationLog.objects.filter(status="RESPONDED")

        if not successful_comms.exists():
            logger.info("No successful communications found for time optimization")
            return "No data available for optimization"

        # Aggregate by hour
        hour_stats = {}
        for hour in range(24):
            # Count successful communications by hour
            hour_count = successful_comms.filter(sent_at__hour=hour).count()
            hour_stats[hour] = hour_count

        # Find top 3 hours
        sorted_hours = sorted(hour_stats.items(), key=lambda x: x[1], reverse=True)
        top_hours = sorted_hours[:3]

        # Aggregate by day of week (0=Monday, 6=Sunday)
        day_stats = {}
        for day in range(7):
            # Count successful communications by day
            day_count = successful_comms.filter(
                sent_at__week_day=day + 1
            ).count()  # Django uses 1-7 for week_day
            day_stats[day] = day_count

        # Find top 3 days
        sorted_days = sorted(day_stats.items(), key=lambda x: x[1], reverse=True)
        top_days = sorted_days[:3]

        # Get day names
        day_names = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        best_days = [day_names[day] for day, count in top_days]

        # Format hours in 12-hour format
        best_hours = [
            f"{hour % 12 or 12} {'AM' if hour < 12 else 'PM'}"
            for hour, count in top_hours
        ]

        logger.info(
            f"Optimal send times: {', '.join(best_hours)} on {', '.join(best_days)}"
        )
        return {
            "best_hours": best_hours,
            "best_days": best_days,
            "hour_stats": hour_stats,
            "day_stats": {day_names[day]: count for day, count in day_stats.items()},
        }

    except Exception as exc:
        logger.error(f"Error finding optimal send times: {str(exc)}")
        self.retry(exc=exc)


@shared_task(
    name="campaigns.tasks.retry_failed_communications",
    bind=True,
    max_retries=3,
    default_retry_delay=300,  # 5 minutes
)
def retry_failed_communications(self, campaign_id=None, max_age_hours=24):
    """
    Retry failed communications that are not too old.

    Args:
        campaign_id: Optional campaign ID to limit retries to a specific campaign
        max_age_hours: Maximum age in hours for retrying communications
    """
    try:
        # Set time threshold for retries
        threshold = timezone.now() - timedelta(hours=max_age_hours)

        # Get failed communications that are recent enough
        query = Q(status="FAILED") & Q(sent_at__gte=threshold)

        # Add campaign filter if specified
        if campaign_id:
            query &= Q(campaign_id=campaign_id)

        failed_comms = CommunicationLog.objects.filter(query)

        if not failed_comms.exists():
            logger.info(
                f"No failed communications to retry for campaign {campaign_id or 'all'}"
            )
            return "No failed communications to retry"

        count = failed_comms.count()
        logger.info(
            f"Retrying {count} failed communications for campaign {campaign_id or 'all'}"
        )

        retried = 0
        for comm in failed_comms:
            # Schedule a new attempt
            send_campaign_communication.delay(
                campaign_id=comm.campaign_id, patient_id=comm.patient_id
            )
            retried += 1

            # Update metadata to track retry
            metadata = comm.metadata.copy() if comm.metadata else {}
            metadata["retried_at"] = timezone.now().isoformat()
            metadata["attempt"] = metadata.get("attempt", 1) + 1
            comm.metadata = metadata
            comm.save(update_fields=["metadata"])

        return (
            f"Retried {retried} failed communications for campaign {campaign_id or 'all'}"
        )

    except Exception as exc:
        logger.error(f"Error retrying failed communications: {str(exc)}")
        self.retry(exc=exc)
