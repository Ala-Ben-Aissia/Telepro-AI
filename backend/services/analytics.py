from django.db.models import Count

from campaigns.models import CommunicationLog
from patients.models import Patient


class AnalyticsService:
    @staticmethod
    def calculate_campaign_effectiveness(campaign_id):
        """Calculate effectiveness metrics for a campaign"""
        logs = CommunicationLog.objects.filter(campaign_id=campaign_id)

        return {
            "total_sent": logs.count(),
            "delivered": logs.filter(status="DELIVERED").count(),
            "responded": logs.filter(status="RESPONDED").count(),
            "failed": logs.filter(status="FAILED").count(),
            "response_rate": logs.filter(status="RESPONDED").count() / logs.count()
            if logs.count() > 0
            else 0,
        }

    @staticmethod
    def get_patient_segments():
        """Get patient segments based on various criteria"""
        return {
            "by_age_group": Patient.objects.values("age_group").annotate(
                count=Count("id")
            ),
            "by_location": Patient.objects.values("location").annotate(count=Count("id")),
            "by_engagement": Patient.objects.values("engagement_score").annotate(
                count=Count("id")
            ),
            "by_language": Patient.objects.values("language_preference").annotate(
                count=Count("id")
            ),
        }
