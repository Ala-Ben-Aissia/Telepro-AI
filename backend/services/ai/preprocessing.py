import numpy as np
from django.db.models import Avg, Count, Q
from django.utils import timezone

from patients.models import Patient


class DataPreprocessingService:
    """
    Service for preprocessing patient data for AI analysis.
    Handles data anonymization, normalization, and feature extraction.
    """

    @staticmethod
    def extract_patient_features(include_only_with_consent=True):
        """
        Extract features from patients for machine learning algorithms.
        Returns anonymized, normalized features suitable for clustering and segmentation.
        """
        # Start with patients that have active consent (if required)
        if include_only_with_consent:
            patients = Patient.objects.filter(has_active_consent=True, is_active=True)
        else:
            patients = Patient.objects.filter(is_active=True)

        if not patients.exists():
            return None, []

        # Initialize lists for features and patient IDs
        features = []
        patient_ids = []

        # Map categorical values to numeric
        gender_mapping = {"M": 0, "F": 1, "O": 2, "N": 3}
        age_mapping = {"0-18": 0, "19-35": 1, "36-50": 2, "51-65": 3, "65+": 4}
        contact_mapping = {"EMAIL": 0, "SMS": 1, "CALL": 2, "NONE": 3}

        # Extract features for each patient
        for patient in patients:
            # Skip patients with missing critical data
            if not patient.age_group:
                continue

            # Basic demographic features
            gender_feature = gender_mapping.get(patient.gender, 3)  # Default to N
            age_feature = age_mapping.get(patient.age_group, 2)  # Default to middle
            contact_feature = contact_mapping.get(patient.preferred_contact_method, 3)

            # Engagement features
            engagement = patient.engagement_score
            contact_rate = patient.successful_contacts / max(1, patient.contact_attempts)

            # Temporal features - recent activity level
            recent_activity = 0
            if patient.last_contacted_at:
                days_since_contact = (timezone.now() - patient.last_contacted_at).days
                # Convert to a 0-1 feature (more recent = higher value)
                recent_activity = max(0, 1 - (days_since_contact / 90))  # 90 days max

            # Combine into feature vector
            patient_features = [
                gender_feature,
                age_feature,
                contact_feature,
                engagement,
                contact_rate,
                recent_activity,
            ]

            features.append(patient_features)
            patient_ids.append(str(patient.id))

        # Convert to numpy array for ML algorithms
        features_array = np.array(features)

        # Normalize features to 0-1 scale
        if features_array.size > 0:
            # Calculate min and max for each feature column
            min_vals = features_array.min(axis=0)
            max_vals = features_array.max(axis=0)

            # Avoid division by zero
            divisor = np.maximum(max_vals - min_vals, 1e-10)

            # Normalize
            features_normalized = (features_array - min_vals) / divisor
        else:
            features_normalized = features_array

        return features_normalized, patient_ids

    @staticmethod
    def get_aggregated_statistics():
        """
        Get anonymized, aggregated statistics about the patient population.
        Complies with GDPR by only returning group-level insights.
        """
        # Only include active patients with consent
        patients = Patient.objects.filter(is_active=True, has_active_consent=True)
        total_count = patients.count()

        if total_count < 10:
            # Not enough patients for meaningful aggregation - privacy risk
            return {
                "status": "insufficient_data",
                "message": "Not enough patient data for aggregated statistics.",
            }

        # Demographics
        gender_distribution = dict(
            patients.values("gender")
            .annotate(count=Count("id"))
            .values_list("gender", "count")
        )

        age_distribution = dict(
            patients.values("age_group")
            .annotate(count=Count("id"))
            .values_list("age_group", "count")
        )

        location_distribution = dict(
            patients.values("location")
            .annotate(count=Count("id"))
            .filter(location__isnull=False)
            .values_list("location", "count")
        )

        # Contact preferences
        contact_method_distribution = dict(
            patients.values("preferred_contact_method")
            .annotate(count=Count("id"))
            .values_list("preferred_contact_method", "count")
        )

        # Engagement metrics
        avg_engagement = (
            patients.aggregate(avg_score=Avg("engagement_score"))["avg_score"] or 0
        )

        # Response rates (using existing campaign data)
        from campaigns.models import CommunicationLog

        comm_stats = CommunicationLog.objects.filter(patient__in=patients).aggregate(
            total=Count("id"),
            responded=Count("id", filter=Q(status="RESPONDED")),
            read=Count("id", filter=Q(status="READ")),
            delivered=Count("id", filter=Q(status="DELIVERED")),
        )

        response_rate = comm_stats["responded"] / max(1, comm_stats["total"])
        delivery_rate = comm_stats["delivered"] / max(1, comm_stats["total"])
        read_rate = comm_stats["read"] / max(1, comm_stats["delivered"])

        # Return the aggregated statistics
        return {
            "total_patients": total_count,
            "demographics": {
                "gender": gender_distribution,
                "age_group": age_distribution,
                "location": location_distribution,
            },
            "preferences": {"contact_method": contact_method_distribution},
            "engagement": {
                "average_score": avg_engagement,
                "response_rate": response_rate,
                "delivery_rate": delivery_rate,
                "read_rate": read_rate,
            },
        }
