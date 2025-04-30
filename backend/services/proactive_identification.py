"""
Proactive Patient Identification Service

This service identifies patients who need follow-up based on their engagement patterns,
medical history, and risk factors.
"""

from datetime import timedelta
from django.utils import timezone
from django.db.models import Q, Count

from patients.models import Patient
from campaigns.models import CommunicationLog
from services.ai.prediction import CampaignPredictionService


class ProactiveIdentificationService:
    """
    Service for identifying patients who need proactive follow-up.

    This service:
    - Identifies inactive patients based on configurable criteria
    - Detects patients with declining engagement
    - Identifies patients with specific follow-up needs
    - Prioritizes patients based on risk factors
    """

    @staticmethod
    def identify_inactive_patients(days_threshold=90, min_risk_score=0.5):
        """
        Identify patients who haven't been contacted in a specified number of days.

        Args:
            days_threshold: Number of days since last contact to consider a patient inactive
            min_risk_score: Minimum risk score to include in results

        Returns:
            Dictionary with inactive patients information
        """
        # Use the existing prediction service as a base
        base_predictions = CampaignPredictionService.predict_inactive_patients(
            days_threshold
        )

        # Filter by minimum risk score
        filtered_predictions = [
            p for p in base_predictions if p["risk_score"] >= min_risk_score
        ]

        # Group by risk level
        high_risk = [p for p in filtered_predictions if p["risk_score"] >= 0.7]
        medium_risk = [p for p in filtered_predictions if 0.5 <= p["risk_score"] < 0.7]

        return {
            "status": "success",
            "days_threshold": days_threshold,
            "min_risk_score": min_risk_score,
            "total_inactive": len(filtered_predictions),
            "high_risk_count": len(high_risk),
            "medium_risk_count": len(medium_risk),
            "patients": filtered_predictions,
        }

    @staticmethod
    def identify_declining_engagement(lookback_days=180, engagement_drop_threshold=0.2):
        """
        Identify patients with declining engagement over time.

        Args:
            lookback_days: Number of days to look back for engagement analysis
            engagement_drop_threshold: Minimum drop in engagement score to consider significant

        Returns:
            Dictionary with patients showing declining engagement
        """
        # Calculate the date threshold
        threshold_date = timezone.now() - timedelta(days=lookback_days)

        # Get patients with sufficient communication history
        patients_with_history = Patient.objects.annotate(
            log_count=Count(
                "communicationlog",
                filter=Q(communicationlog__sent_at__gte=threshold_date),
            )
        ).filter(log_count__gte=3)  # At least 3 communications to analyze trend

        declining_patients = []

        # Analyze each patient's engagement trend
        for patient in patients_with_history:
            # Get communication logs in chronological order
            logs = CommunicationLog.objects.filter(
                patient=patient, sent_at__gte=threshold_date
            ).order_by("sent_at")

            # Skip if not enough logs
            if logs.count() < 3:
                continue

            # Divide logs into two periods for comparison
            midpoint = logs.count() // 2
            early_logs = logs[:midpoint]
            recent_logs = logs[midpoint:]

            # Calculate engagement metrics for each period
            early_response_rate = (
                early_logs.filter(status="RESPONDED").count() / early_logs.count()
            )
            recent_response_rate = (
                recent_logs.filter(status="RESPONDED").count() / recent_logs.count()
            )

            # Calculate engagement drop
            engagement_drop = early_response_rate - recent_response_rate

            # If engagement has dropped significantly, add to results
            if engagement_drop >= engagement_drop_threshold:
                declining_patients.append(
                    {
                        "patient_id": str(patient.id),
                        "username": patient.user.username,
                        "engagement_score": patient.engagement_score,
                        "early_response_rate": early_response_rate,
                        "recent_response_rate": recent_response_rate,
                        "engagement_drop": engagement_drop,
                        "last_contacted_at": patient.last_contacted_at.isoformat()
                        if patient.last_contacted_at
                        else None,
                        "preferred_contact_method": patient.preferred_contact_method,
                        "risk_level": "high" if engagement_drop >= 0.4 else "medium",
                    }
                )

        # Sort by engagement drop (highest first)
        declining_patients.sort(key=lambda x: x["engagement_drop"], reverse=True)

        return {
            "status": "success",
            "lookback_days": lookback_days,
            "engagement_drop_threshold": engagement_drop_threshold,
            "total_patients": len(declining_patients),
            "patients": declining_patients,
        }

    @staticmethod
    def identify_follow_up_candidates(condition_type=None, days_since_last_contact=60):
        """
        Identify patients who need specific follow-up based on condition type.

        Args:
            condition_type: Type of condition to filter by (e.g., "vaccination", "dental")
            days_since_last_contact: Minimum days since last contact

        Returns:
            Dictionary with patients needing follow-up
        """
        # Base query - patients with active consent who haven't been contacted recently
        threshold_date = timezone.now() - timedelta(days=days_since_last_contact)

        base_query = Q(has_active_consent=True, is_active=True, anonymized=False) & (
            Q(last_contacted_at__lt=threshold_date) | Q(last_contacted_at__isnull=True)
        )

        # Add condition-specific filters
        if condition_type:
            condition_type = condition_type.lower()

            if condition_type == "vaccination":
                # For vaccination, prioritize certain age groups
                base_query &= Q(age_group__in=["0-18", "65+"])
            elif condition_type == "dental":
                # For dental, no specific demographic filters
                pass
            elif condition_type == "chronic":
                # For chronic conditions, prioritize older patients
                base_query &= Q(age_group__in=["51-65", "65+"])

        # Get matching patients
        patients = Patient.objects.filter(base_query)

        # Format results
        follow_up_candidates = []
        for patient in patients:
            # Calculate priority score based on days since contact and engagement
            days_factor = 1.0
            if patient.last_contacted_at:
                days_since_contact = (timezone.now() - patient.last_contacted_at).days
                days_factor = min(1.0, days_since_contact / 365)  # Cap at 1 year

            priority_score = 0.7 * days_factor + 0.3 * (1 - patient.engagement_score)

            follow_up_candidates.append(
                {
                    "patient_id": str(patient.id),
                    "username": patient.user.username,
                    "age_group": patient.age_group,
                    "gender": patient.gender,
                    "location": patient.location,
                    "language_preference": patient.language_preference,
                    "last_contacted_at": patient.last_contacted_at.isoformat()
                    if patient.last_contacted_at
                    else None,
                    "days_since_contact": (
                        timezone.now() - patient.last_contacted_at
                    ).days
                    if patient.last_contacted_at
                    else None,
                    "engagement_score": patient.engagement_score,
                    "preferred_contact_method": patient.preferred_contact_method,
                    "priority_score": priority_score,
                    "priority_level": "high"
                    if priority_score >= 0.7
                    else "medium"
                    if priority_score >= 0.4
                    else "low",
                }
            )

        # Sort by priority score (highest first)
        follow_up_candidates.sort(key=lambda x: x["priority_score"], reverse=True)

        return {
            "status": "success",
            "condition_type": condition_type,
            "days_since_last_contact": days_since_last_contact,
            "total_candidates": len(follow_up_candidates),
            "candidates": follow_up_candidates,
        }

    @staticmethod
    def get_follow_up_recommendations(patient_id):
        """
        Get personalized follow-up recommendations for a specific patient.

        Args:
            patient_id: ID of the patient

        Returns:
            Dictionary with follow-up recommendations
        """
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return {"status": "error", "message": "Patient not found"}

        # Get patient's communication logs
        logs = CommunicationLog.objects.filter(patient=patient).order_by("-sent_at")

        # Calculate basic metrics
        total_communications = logs.count()
        response_rate = (
            logs.filter(status="RESPONDED").count() / total_communications
            if total_communications > 0
            else 0
        )

        # Determine best contact method based on response history
        contact_method_stats = {}
        for method in ["EMAIL", "SMS", "CALL"]:
            method_logs = logs.filter(communication_type=method)
            method_count = method_logs.count()

            if method_count > 0:
                method_response_rate = (
                    method_logs.filter(status="RESPONDED").count() / method_count
                )
                contact_method_stats[method] = {
                    "count": method_count,
                    "response_rate": method_response_rate,
                }

        # Determine best contact method
        best_method = patient.preferred_contact_method
        best_rate = 0

        for method, stats in contact_method_stats.items():
            if stats["count"] >= 3 and stats["response_rate"] > best_rate:
                best_method = method
                best_rate = stats["response_rate"]

        # Determine best contact time based on successful responses
        responded_logs = logs.filter(status="RESPONDED", sent_at__isnull=False)

        time_periods = {"morning": 0, "afternoon": 0, "evening": 0}

        for log in responded_logs:
            hour = log.sent_at.hour
            if 6 <= hour < 12:
                time_periods["morning"] += 1
            elif 12 <= hour < 18:
                time_periods["afternoon"] += 1
            else:
                time_periods["evening"] += 1

        # Find best time period
        best_time = (
            max(time_periods.items(), key=lambda x: x[1])[0]
            if any(time_periods.values())
            else "afternoon"
        )

        # Generate recommendations
        recommendations = []

        # Contact method recommendation
        if best_method != patient.preferred_contact_method and best_rate > 0:
            recommendations.append(
                f"Consider using {best_method} for communications (response rate: {best_rate:.1%})"
            )

        # Contact timing recommendation
        recommendations.append(f"Best time to contact: {best_time}")

        # Engagement recommendations
        if response_rate < 0.3:
            recommendations.append(
                "Low response rate. Consider more personalized messaging."
            )

        # Follow-up frequency recommendation
        if patient.last_contacted_at:
            days_since_contact = (timezone.now() - patient.last_contacted_at).days
            if days_since_contact > 180:
                recommendations.append(
                    "Patient hasn't been contacted in over 6 months. Consider high-priority follow-up."
                )
            elif days_since_contact > 90:
                recommendations.append(
                    "Patient hasn't been contacted in over 3 months. Consider follow-up."
                )

        # Age-specific recommendations
        if patient.age_group == "65+":
            recommendations.append(
                "Older patient may benefit from more frequent check-ins."
            )

        return {
            "status": "success",
            "patient_id": str(patient_id),
            "username": patient.user.username,
            "engagement_score": patient.engagement_score,
            "response_rate": response_rate,
            "total_communications": total_communications,
            "last_contacted_at": patient.last_contacted_at.isoformat()
            if patient.last_contacted_at
            else None,
            "preferred_contact_method": patient.preferred_contact_method,
            "best_contact_method": best_method,
            "best_contact_time": best_time,
            "contact_method_stats": contact_method_stats,
            "recommendations": recommendations,
        }
