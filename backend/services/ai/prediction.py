from datetime import datetime

from django.utils import timezone

from campaigns.models import Campaign, CommunicationLog
from patients.models import Patient


class CampaignPredictionService:
    """
    Service for predicting campaign effectiveness and patient responses.
    """

    @staticmethod
    def predict_campaign_effectiveness(campaign_id):
        """
        Predict the likely effectiveness of a campaign based on historical data.

        Returns:
            Predicted response rate and confidence level.
        """
        campaign = Campaign.objects.get(id=campaign_id)

        # Get historical data from similar campaigns
        similar_campaigns = Campaign.objects.filter(
            category=campaign.category, is_active=True
        ).exclude(id=campaign_id)

        if not similar_campaigns.exists():
            return {
                "status": "insufficient_data",
                "message": "No similar campaigns found for prediction.",
            }

        # Collect historical response data
        campaign_stats = []

        for similar_campaign in similar_campaigns:
            logs = CommunicationLog.objects.filter(campaign=similar_campaign)
            total = logs.count()

            if total < 10:  # Skip campaigns with too few communications
                continue

            responded = logs.filter(status="RESPONDED").count()
            response_rate = responded / total if total > 0 else 0

            campaign_stats.append(
                {
                    "campaign_id": similar_campaign.id,
                    "response_rate": response_rate,
                    "total_sent": total,
                    "age_groups": similar_campaign.target_age_groups,
                    "locations": similar_campaign.target_locations,
                    "languages": similar_campaign.target_languages,
                }
            )

        if not campaign_stats:
            return {
                "status": "insufficient_data",
                "message": "Not enough data from similar campaigns.",
            }

        # Calculate average response rate from similar campaigns
        total_responses = sum(
            stat["response_rate"] * stat["total_sent"] for stat in campaign_stats
        )
        total_communications = sum(stat["total_sent"] for stat in campaign_stats)
        avg_response_rate = (
            total_responses / total_communications if total_communications > 0 else 0
        )

        # Adjust prediction based on current campaign specifics
        # This is a simplified model - a real implementation would use more sophisticated ML
        adjustment_factor = 1.0

        # More specific targeting might increase effectiveness
        if len(campaign.target_age_groups) < 3:
            adjustment_factor *= 1.1

        if len(campaign.target_locations) < 3:
            adjustment_factor *= 1.05

        # Time-based adjustments
        current_month = datetime.now().month
        if 9 <= current_month <= 11:  # Fall months often have higher engagement
            adjustment_factor *= 1.1
        elif 6 <= current_month <= 8:  # Summer months often have lower engagement
            adjustment_factor *= 0.9

        # Calculate predicted response rate
        predicted_rate = min(0.95, avg_response_rate * adjustment_factor)

        # Calculate confidence level based on amount of data
        confidence = min(0.9, total_communications / 1000) * 100

        return {
            "status": "success",
            "predicted_response_rate": round(predicted_rate * 100, 2),
            "confidence_level": round(confidence, 2),
            "similar_campaigns_count": len(campaign_stats),
            "historical_avg_response_rate": round(avg_response_rate * 100, 2),
            "recommended_improvements": CampaignPredictionService._get_recommendations(
                campaign, predicted_rate
            ),
        }

    @staticmethod
    def _get_recommendations(campaign, predicted_rate):
        """Generate recommendations to improve campaign effectiveness"""
        recommendations = []

        if not campaign.email_template or len(campaign.email_template) < 100:
            recommendations.append("Enhance email template with more detailed content")

        if not campaign.sms_template or len(campaign.sms_template) < 20:
            recommendations.append("Create a more compelling SMS message")

        if predicted_rate < 0.1:
            recommendations.append(
                "Consider narrowing target audience for better engagement"
            )

        if len(campaign.target_age_groups) > 3:
            recommendations.append(
                "Target fewer age groups for more personalized messaging"
            )

        if len(campaign.target_languages) > 2:
            recommendations.append(
                "Consider creating language-specific campaign variants"
            )

        return recommendations

    @staticmethod
    def predict_patient_response(patient_id, campaign_id):
        """
        Predict whether a specific patient is likely to respond to a campaign.

        Returns:
            Probability of patient response and key factors.
        """
        patient = Patient.objects.get(id=patient_id)
        campaign = Campaign.objects.get(id=campaign_id)

        # Check if patient matches campaign criteria
        matches_age_group = any(
            ag == patient.age_group for ag in campaign.target_age_groups
        )
        matches_location = any(
            loc == patient.location for loc in campaign.target_locations
        )
        matches_language = any(
            lang == patient.language_preference for lang in campaign.target_languages
        )

        # Basic criteria match score (0-1)
        criteria_score = (
            (0.4 if matches_age_group else 0)
            + (0.3 if matches_location else 0)
            + (0.3 if matches_language else 0)
        )

        # Historical engagement score (0-1)
        engagement_score = patient.engagement_score

        # Communication preference match (0-1)
        method_match = 0
        if campaign.email_template and patient.preferred_contact_method == "EMAIL":
            method_match = 1
        elif campaign.sms_template and patient.preferred_contact_method == "SMS":
            method_match = 1

        # Recent activity (recency effect)
        recency_score = 0
        if patient.last_campaign_response:
            days_since_response = (timezone.now() - patient.last_campaign_response).days
            recency_score = max(
                0, 1 - (days_since_response / 90)
            )  # 0-1 scale, 90 days max

        # Calculate response probability
        # This is a simple weighted formula - a real implementation would use machine learning
        response_probability = (
            0.3 * criteria_score
            + 0.3 * engagement_score
            + 0.2 * method_match
            + 0.2 * recency_score
        )

        # Determine key factors
        key_factors = []
        if criteria_score > 0.7:
            key_factors.append("Strong match with campaign criteria")
        elif criteria_score < 0.3:
            key_factors.append("Poor match with campaign criteria")

        if engagement_score > 0.7:
            key_factors.append("High historical engagement")
        elif engagement_score < 0.3:
            key_factors.append("Low historical engagement")

        if method_match > 0:
            key_factors.append("Preferred contact method matches campaign")
        else:
            key_factors.append("Preferred contact method doesn't match campaign")

        if recency_score > 0.7:
            key_factors.append("Recently active with campaigns")
        elif recency_score < 0.3:
            key_factors.append("Not recently active with campaigns")

        return {
            "patient_id": str(patient.id),
            "campaign_id": campaign_id,
            "response_probability": round(response_probability * 100, 2),
            "key_factors": key_factors,
            "matches_criteria": {
                "age_group": matches_age_group,
                "location": matches_location,
                "language": matches_language,
            },
        }
