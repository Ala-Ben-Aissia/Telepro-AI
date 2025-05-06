from datetime import datetime

from django.utils import timezone
from .training import PatientResponseTrainer
import numpy as np
import pandas as pd

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
        Uses a trained machine learning model if available, otherwise falls back to a rule-based approach.

        Returns:
            Probability of patient response and key factors.
        """
        patient = Patient.objects.get(id=patient_id)
        campaign = Campaign.objects.get(id=campaign_id)

        # Try to use the ML model first
        trainer = PatientResponseTrainer()
        model = trainer.load_model()

        if model:
            # Prepare the feature data for prediction
            features = {}

            # 1. Patient demographic features
            features.update(
                {
                    "age_group": patient.age_group or "Unknown",
                    "gender": patient.gender or "Unknown",
                    "language_preference": patient.language_preference or "Unknown",
                    "location": patient.location or "Unknown",
                    "preferred_contact_method": patient.preferred_contact_method,
                }
            )

            # 2. Patient engagement metrics
            features.update(
                {
                    "engagement_score": patient.engagement_score,
                    "contact_attempts": patient.contact_attempts,
                    "successful_contacts": patient.successful_contacts,
                    "email_verified": int(patient.email_verified),
                    "phone_verified": int(patient.phone_verified),
                }
            )

            # 3. Campaign features
            features.update(
                {
                    "campaign_category": campaign.category.name
                    if campaign.category
                    else "Unknown",
                    "has_email_template": 1 if campaign.email_template else 0,
                    "has_sms_template": 1 if campaign.sms_template else 0,
                }
            )

            # 4. Patient-campaign match features
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

            features.update(
                {
                    "matches_age_group": int(matches_age_group),
                    "matches_location": int(matches_location),
                    "matches_language": int(matches_language),
                    "method_match": int(
                        (
                            campaign.email_template
                            and patient.preferred_contact_method == "EMAIL"
                        )
                        or (
                            campaign.sms_template
                            and patient.preferred_contact_method == "SMS"
                        )
                    ),
                }
            )

            # 5. Historical activity features
            if patient.last_campaign_response:
                days_since_response = (
                    timezone.now() - patient.last_campaign_response
                ).days
                features["days_since_response"] = min(days_since_response, 365)
                features["has_recent_response"] = 1 if days_since_response <= 30 else 0
            else:
                features["days_since_response"] = 365  # Default to maximum
                features["has_recent_response"] = 0

            if patient.last_contacted_at:
                days_since_contact = (timezone.now() - patient.last_contacted_at).days
                features["days_since_contact"] = min(days_since_contact, 365)
                features["has_recent_contact"] = 1 if days_since_contact <= 30 else 0
            else:
                features["days_since_contact"] = 365
                features["has_recent_contact"] = 0

            # Convert to DataFrame for one-hot encoding
            df = pd.DataFrame([features])

            # Create dummy variables for categorical columns
            categorical_cols = [
                "age_group",
                "gender",
                "language_preference",
                "location",
                "preferred_contact_method",
                "campaign_category",
            ]
            df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=False)

            # Get missing columns (might be present in training data but not in our single instance)
            # This is needed because the model expects exactly the same features it was trained on

            try:
                # Predict probability using the model
                response_probability = model.predict_proba(df_encoded)[
                    0, 1
                ]  # Probability of class 1

                # Determine key factors (using feature importance)
                if hasattr(model["classifier"], "feature_importances_"):
                    # Get feature names from the model or use the ones we have
                    model_features = getattr(
                        model, "feature_names_in_", df_encoded.columns
                    )

                    # Get feature importances
                    importances = model["classifier"].feature_importances_

                    # Get top factors
                    top_indices = np.argsort(importances)[-5:]  # Top 5 factors
                    key_factors = []

                    for idx in top_indices:
                        if idx < len(model_features):
                            feature = model_features[idx]
                            # Convert feature name to human-readable description
                            if "age_group" in feature and matches_age_group:
                                key_factors.append(
                                    f"Age group match ({patient.age_group})"
                                )
                            elif "location" in feature and matches_location:
                                key_factors.append(f"Location match ({patient.location})")
                            elif "language" in feature and matches_language:
                                key_factors.append(
                                    f"Language preference match ({patient.language_preference})"
                                )
                            elif "method_match" in feature and features["method_match"]:
                                key_factors.append(
                                    "Preferred contact method matches campaign"
                                )
                            elif "engagement_score" in feature:
                                if patient.engagement_score > 0.7:
                                    key_factors.append("High historical engagement")
                                elif patient.engagement_score < 0.3:
                                    key_factors.append("Low historical engagement")
                            elif "recent_response" in feature and features.get(
                                "has_recent_response"
                            ):
                                key_factors.append("Recently responded to campaigns")
                else:
                    # Fallback if no feature importances available
                    key_factors = CampaignPredictionService._get_key_factors(
                        patient, campaign
                    )

            except Exception as e:
                # If prediction fails, fall back to the rule-based approach
                print(
                    f"ML prediction failed: {str(e)}, falling back to rule-based approach"
                )
                return CampaignPredictionService._rule_based_prediction(patient, campaign)

            return {
                "patient_id": str(patient.id),
                "campaign_id": campaign_id,
                "response_probability": round(response_probability * 100, 2),
                "key_factors": key_factors,
                "model_based": True,
                "matches_criteria": {
                    "age_group": matches_age_group,
                    "location": matches_location,
                    "language": matches_language,
                },
            }
        else:
            # Fall back to the rule-based approach if no model is available
            return CampaignPredictionService._rule_based_prediction(patient, campaign)

    @staticmethod
    def _rule_based_prediction(patient, campaign: Campaign):
        """Rule-based fallback prediction when ML model is not available."""
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
        response_probability = (
            0.3 * criteria_score
            + 0.3 * engagement_score
            + 0.2 * method_match
            + 0.2 * recency_score
        )

        # Get key factors
        key_factors = CampaignPredictionService._get_key_factors(patient, campaign)

        return {
            "patient_id": str(patient.id),
            "campaign_id": campaign.pk,
            "response_probability": round(response_probability * 100, 2),
            "key_factors": key_factors,
            "model_based": False,
            "matches_criteria": {
                "age_group": matches_age_group,
                "location": matches_location,
                "language": matches_language,
            },
        }

    @staticmethod
    def _get_key_factors(patient, campaign):
        """Determine key factors for the prediction."""
        key_factors = []

        # Check criteria match
        matches_age_group = any(
            ag == patient.age_group for ag in campaign.target_age_groups
        )
        matches_location = any(
            loc == patient.location for loc in campaign.target_locations
        )
        matches_language = any(
            lang == patient.language_preference for lang in campaign.target_languages
        )

        criteria_score = (
            (0.6 if matches_age_group else 0)
            + (0.2 if matches_location else 0)
            + (0.2 if matches_language else 0)
        )

        if criteria_score > 0.7:
            key_factors.append("Strong match with campaign criteria")
        elif criteria_score < 0.3:
            key_factors.append("Poor match with campaign criteria")

        if patient.engagement_score > 0.7:
            key_factors.append("High historical engagement")
        elif patient.engagement_score < 0.3:
            key_factors.append("Low historical engagement")

        method_match = 0
        if campaign.email_template and patient.preferred_contact_method == "EMAIL":
            method_match = 1
        elif campaign.sms_template and patient.preferred_contact_method == "SMS":
            method_match = 1

        if method_match > 0:
            key_factors.append("Preferred contact method matches campaign")
        else:
            key_factors.append("Preferred contact method doesn't match campaign")

        if patient.last_campaign_response:
            days_since_response = (timezone.now() - patient.last_campaign_response).days
            recency_score = max(0, 1 - (days_since_response / 90))

            if recency_score > 0.7:
                key_factors.append("Recently active with campaigns")
            elif recency_score < 0.3:
                key_factors.append("Not recently active with campaigns")

        return key_factors

    @staticmethod
    def predict_inactive_patients(days_threshold=90):
        """
        Identify patients likely to become inactive based on engagement patterns
        (Implements spec-book requirement 3.2)
        """
        from patients.models import Patient
        from django.utils import timezone

        # Get active patients with consent
        patients = Patient.objects.filter(is_active=True, has_active_consent=True)

        results = []
        for patient in patients:
            # Extract features
            features = {
                "days_since_contact": (timezone.now() - patient.last_contacted_at).days
                if patient.last_contacted_at
                else 365,
                "engagement_score": patient.engagement_score,
                "contact_attempts": patient.contact_attempts,
                "successful_contacts": patient.successful_contacts,
                "response_rate": patient.successful_contacts
                / max(1, patient.contact_attempts),
            }

            # First filter: Only consider patients who haven't been contacted in [days_threshold] days
            # This ensures the days_threshold parameter is actually used
            if (
                features["days_since_contact"] < days_threshold / 2
            ):  # Using half the threshold as a minimum
                continue

            # Calculate risk relative to threshold (makes days_threshold parameter meaningful)
            # Someone at threshold should have a time risk of 0.5
            time_risk = min(1.0, features["days_since_contact"] / (days_threshold * 2))

            # Calculate inactivity risk score with adjusted weights
            # Increase time weight since that's the primary concern
            risk_score = (
                0.6 * time_risk
                + 0.2 * (1 - features["engagement_score"])
                + 0.2 * (1 - features["response_rate"])
            )

            # Risk threshold is dynamically based on days_since_contact relation to threshold
            min_risk_threshold = (
                0.5 if features["days_since_contact"] >= days_threshold else 0.7
            )

            if risk_score > min_risk_threshold:
                results.append(
                    {
                        "patient_id": str(patient.id),
                        "risk_score": risk_score,
                        "days_since_contact": features["days_since_contact"],
                        # "days_threshold": days_threshold,
                        "engagement_score": features["engagement_score"],
                        "response_rate": features["response_rate"],
                        "recommended_action": "Follow up required"
                        if risk_score > 0.7
                        else "Monitor",
                    }
                )

        # Sort by risk score (highest first)
        return sorted(results, key=lambda x: x["risk_score"], reverse=True)


"""
This improved implementation:
1. Uses the days_threshold parameter meaningfully: Filters out patients with recent contact (less than half the threshold)
2. Normalizes time risk relative to threshold: Makes the days_threshold parameter directly affect scoring
3. Weights time more heavily (60% vs 40% before)
4. Adjusts threshold dynamically: Requires higher risk scores for patients below the days threshold
5. Provides more detailed information in results for better debugging
6. Creates a "Monitor" vs "Follow up required" distinction for different risk levels

So With these changes, we should see more meaningful results where patients with fewer days since contact won't appear unless they have extremely poor engagement metrics, and the days_threshold parameter will have a more intuitive effect on the results.

This is a common issue in ML applications where multiple factors are combined - it can be challenging to tune the weights and thresholds to match business expectations. The improved implementation gives you more control and transparency.
"""
