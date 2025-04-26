"""Preprocessing utilities for AI services"""

__all__ = ["DataPreprocessingService", "calculate_response_trend"]

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from django.utils import timezone
from datetime import timedelta
import logging
import joblib
import os

logger = logging.getLogger(__name__)

# --- Feature Engineering Helper Functions ---


def calculate_response_trend(patient, window_days=90):
    """
    Calculate the trend in patient response rate over time.
    A positive trend means improving response rate, negative means declining.

    Args:
        patient: Patient instance
        window_days: Number of days to analyze for trend

    Returns:
        float: Trend value between -1 and 1
    """
    from campaigns.models import CommunicationLog

    now = timezone.now()
    window_start = now - timedelta(days=window_days)

    # Get communications in the window
    logs = CommunicationLog.objects.filter(
        patient=patient, sent_at__gte=window_start
    ).order_by("sent_at")

    if logs.count() < 5:  # Need minimum data points
        return 0.0

    # Split window into two halves
    mid_point = window_start + timedelta(days=window_days // 2)
    first_half = logs.filter(sent_at__lt=mid_point)
    second_half = logs.filter(sent_at__gte=mid_point)

    def calc_response_rate(queryset):
        total = queryset.count()
        if total == 0:
            return 0.0
        responded = queryset.filter(status="RESPONDED").count()
        return responded / total

    # Calculate response rates for each half
    rate1 = calc_response_rate(first_half)
    rate2 = calc_response_rate(second_half)

    # Calculate trend (-1 to 1)
    trend = rate2 - rate1

    # Normalize to -1 to 1 range
    return max(min(trend, 1.0), -1.0)


def encode_age_group(age_group):
    """
    Encode age group as an ordinal integer for feature engineering.
    """
    mapping = {
        "0-18": 0,
        "19-35": 1,
        "36-50": 2,
        "51-65": 3,
        "65+": 4,
        "UNKNOWN": -1,
        "Unknown": -1,
        None: -1,
    }
    return mapping.get(age_group, -1)


def calculate_campaign_match_score(patient):
    """
    Calculate a match score (0-1) between patient and their most recent campaign.
    If no campaign, returns 0.
    """
    from campaigns.models import CommunicationLog

    # Find the most recent campaign communication for this patient
    log = (
        CommunicationLog.objects.filter(patient=patient, campaign__isnull=False)
        .order_by("-sent_at")
        .first()
    )
    if not log or not log.campaign:
        return 0.0

    campaign = log.campaign
    score = 0.0
    if patient.age_group and campaign.target_age_groups:
        if patient.age_group in campaign.target_age_groups:
            score += 0.4
    if patient.location and campaign.target_locations:
        if patient.location in campaign.target_locations:
            score += 0.3
    if patient.language_preference and campaign.target_languages:
        if patient.language_preference in campaign.target_languages:
            score += 0.3
    return round(score, 2)


class DataPreprocessingService:
    """
    Service for preprocessing patient data for AI analysis.
    Handles data extraction, transformation, normalization and feature engineering.
    """

    @staticmethod
    def create_preprocessing_pipeline():
        """
        Create a reusable scikit-learn pipeline for preprocessing patient data

        Returns:
            tuple: (pipeline, feature_columns)
        """
        # Define feature types
        numeric_features = [
            "engagement_score",
            "contact_rate",
            "days_since_contact",
            "days_since_response",
            "total_communications_90d",
            "read_rate_90d",
            "response_rate_90d",
        ]

        binary_features = [
            "email_verified",
            "phone_verified",
            "recent_contact",
            "recent_response",
        ]

        categorical_features = [
            "gender",
            "age_group",
            "location",
            "preferred_contact_method",
            "language_preference",
            "postal_region",
        ]

        # Create preprocessing steps
        numeric_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="mean")),
                ("scaler", StandardScaler()),
            ]
        )

        binary_transformer = Pipeline(
            steps=[("imputer", SimpleImputer(strategy="constant", fill_value=0))]
        )

        categorical_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("encoder", OneHotEncoder(sparse_output=False, handle_unknown="ignore")),
            ]
        )

        # Combine all transformers in a ColumnTransformer
        preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, numeric_features),
                ("bin", binary_transformer, binary_features),
                ("cat", categorical_transformer, categorical_features),
            ],
            remainder="drop",  # Drop any columns not specified
        )

        # Create the full pipeline
        pipeline = Pipeline(steps=[("preprocessor", preprocessor)])

        # All features
        feature_columns = numeric_features + binary_features + categorical_features

        return pipeline, feature_columns

    @staticmethod
    def extract_patient_features(
        include_only_with_consent=True,
        pipeline=None,
        return_dataframe=False,
        include_raw_data=False,
    ):
        """
        Extract features from patients for machine learning algorithms using a pipeline.

        Args:
            include_only_with_consent (bool): Only include patients with active consent
            pipeline: Optional pre-fit preprocessing pipeline
            return_dataframe (bool): Whether to return a pandas DataFrame instead of arrays
            include_raw_data (bool): Whether to include raw data before preprocessing

        Returns:
            tuple: (features, patient_ids, pipeline) or DataFrame if return_dataframe=True
        """
        from patients.models import Patient
        from campaigns.models import CommunicationLog

        # Start with patients that have active consent (if required)
        qs = Patient.objects.filter(is_active=True)
        if include_only_with_consent:
            qs = qs.filter(has_active_consent=True)

        if not qs.exists():
            # Return appropriate empty results based on parameters
            if return_dataframe:
                empty_df = pd.DataFrame()
                if include_raw_data:
                    return empty_df, empty_df
                return empty_df
            else:
                if include_raw_data:
                    return np.array([]), [], None, [], pd.DataFrame()
                return np.array([]), [], None, []

        # Define reference timestamps for temporal features
        now = timezone.now()
        # thirty_days_ago = now - timedelta(days=30)
        ninety_days_ago = now - timedelta(days=90)

        # Extract features for each patient
        data = []
        patient_ids = []

        for patient in qs:
            # Skip patients with missing critical data or anonymized
            if patient.anonymized:
                continue

            patient_data = {}
            patient_ids.append(str(patient.id))

            # Basic demographic features
            patient_data["gender"] = patient.gender or "N"
            patient_data["age_group"] = patient.age_group or "UNKNOWN"
            patient_data["location"] = patient.location or "UNKNOWN"
            patient_data["preferred_contact_method"] = patient.preferred_contact_method
            patient_data["language_preference"] = patient.language_preference or "fr"
            patient_data["days_active"] = (now - patient.created_at).days
            patient_data["response_rate_trend"] = calculate_response_trend(
                patient
            )  # Implement this function

            # Add interaction features
            patient_data["engagement_by_age"] = patient_data[
                "engagement_score"
            ] * encode_age_group(patient_data["age_group"])
            patient_data["match_score"] = calculate_campaign_match_score(
                patient
            )  # Implement this

            # Generate postal region from postal code
            if patient.postal_code and len(patient.postal_code) >= 2:
                patient_data["postal_region"] = patient.postal_code[:2]
            else:
                patient_data["postal_region"] = "XX"

            # Communication and engagement metrics
            patient_data["engagement_score"] = float(patient.engagement_score)
            patient_data["contact_rate"] = patient.successful_contacts / max(
                1, patient.contact_attempts
            )
            patient_data["email_verified"] = int(patient.email_verified)
            patient_data["phone_verified"] = int(patient.phone_verified)

            # Recent activity metrics
            if patient.last_contacted_at:
                days_since_contact = (now - patient.last_contacted_at).days
                patient_data["days_since_contact"] = min(days_since_contact, 365)
                patient_data["recent_contact"] = 1 if days_since_contact <= 30 else 0
            else:
                patient_data["days_since_contact"] = 365  # Default to max
                patient_data["recent_contact"] = 0

            if patient.last_campaign_response:
                days_since_response = (now - patient.last_campaign_response).days
                patient_data["days_since_response"] = min(days_since_response, 365)
                patient_data["recent_response"] = 1 if days_since_response <= 30 else 0
            else:
                patient_data["days_since_response"] = 365  # Default to max
                patient_data["recent_response"] = 0

            # Get communication logs for additional features
            recent_logs = CommunicationLog.objects.filter(
                patient=patient, sent_at__gte=ninety_days_ago
            )

            # Calculate communication engagement metrics
            total_recent = recent_logs.count()
            patient_data["total_communications_90d"] = total_recent

            if total_recent > 0:
                # Calculate read and response rates
                read_count = recent_logs.filter(status="READ").count()
                responded_count = recent_logs.filter(status="RESPONDED").count()

                patient_data["read_rate_90d"] = read_count / total_recent
                patient_data["response_rate_90d"] = responded_count / total_recent
            else:
                patient_data["read_rate_90d"] = 0
                patient_data["response_rate_90d"] = 0

            # Add to data collection
            data.append(patient_data)

        # Convert to DataFrame
        if not data:
            if return_dataframe:
                empty_df = pd.DataFrame()
                if include_raw_data:
                    return empty_df, empty_df
                return empty_df
            else:
                empty_features = np.array([])
                empty_ids = []
                if include_raw_data:
                    empty_df = pd.DataFrame()
                    return empty_features, empty_ids, None, [], empty_df
                return empty_features, empty_ids, None, []

        df = pd.DataFrame(data)

        # Create or use preprocessing pipeline
        if pipeline is None:
            pipeline, feature_columns = (
                DataPreprocessingService.create_preprocessing_pipeline()
            )

            # Ensure all expected columns exist (handle case where some are missing)
            for col in feature_columns:
                if col not in df.columns:
                    df[col] = np.nan

            # Fit and transform the data
            features = pipeline.fit_transform(df)
        else:
            # Ensure all expected columns exist (get columns from fitted pipeline)
            column_transformer = pipeline.named_steps["preprocessor"]
            feature_columns = []
            for name, _, cols in column_transformer.transformers_:
                feature_columns.extend(cols)

            for col in feature_columns:
                if col not in df.columns:
                    df[col] = np.nan

            # Use provided pipeline to transform
            features = pipeline.transform(df)

        # Get feature names
        feature_names = []
        ct = pipeline.named_steps["preprocessor"]

        # Get numeric feature names (pass through)
        numeric_cols = ct.transformers_[0][2]
        feature_names.extend(numeric_cols)

        # Get binary feature names (pass through)
        binary_cols = ct.transformers_[1][2]
        feature_names.extend(binary_cols)

        # Get encoded categorical feature names
        categorical_cols = ct.transformers_[2][2]
        encoder = ct.named_transformers_["cat"].named_steps["encoder"]
        encoded_names = encoder.get_feature_names_out(categorical_cols)
        feature_names.extend(encoded_names)

        # Return in requested format
        if return_dataframe:
            result_df = pd.DataFrame(features, columns=feature_names, index=patient_ids)

            if include_raw_data:
                # Include original data columns
                df.index = patient_ids
                return result_df, df

            return result_df

        if include_raw_data:
            return features, patient_ids, pipeline, feature_names, df

        return features, patient_ids, pipeline, feature_names

    @staticmethod
    def save_pipeline(pipeline, filename="patient_pipeline.joblib"):
        """
        Save preprocessing pipeline to a file for later reuse.
        """
        try:
            # Get directory from filename or use default models dir
            directory = os.path.dirname(filename)
            if directory:
                os.makedirs(directory, exist_ok=True)
            else:
                models_dir = os.path.join("models")
                print(f"models dir: {models_dir}")
                os.makedirs(models_dir, exist_ok=True)
                filename = os.path.join(models_dir, filename)

            # Save pipeline
            joblib.dump(pipeline, filename)
            return True
        except Exception as e:
            logger.error(f"Error saving pipeline: {str(e)}")
            return False

    @staticmethod
    def load_pipeline(filename="patient_pipeline.joblib"):
        """
        Load preprocessing pipeline from a file.
        """
        try:
            # Check if path exists directly
            if not os.path.exists(filename):
                # Try with models directory
                models_dir = os.path.join("models")
                alternate_path = os.path.join(models_dir, filename)
                if os.path.exists(alternate_path):
                    filename = alternate_path

            pipeline = joblib.load(filename)
            return pipeline
        except Exception as e:
            logger.error(f"Error loading pipeline: {str(e)}")
            return None

    @staticmethod
    def get_feature_importance(features, feature_names, n_top=10):
        """
        Get feature importance using a Random Forest model.

        Args:
            features: Feature matrix
            feature_names: List of feature names
            n_top: Number of top features to return

        Returns:
            DataFrame with feature importance scores
        """
        from sklearn.ensemble import RandomForestClassifier

        # Skip if no features or feature names
        if features is None or len(features) == 0 or len(feature_names) == 0:
            return pd.DataFrame(columns=["feature", "importance"])

        # Create synthetic target by clustering
        from sklearn.cluster import KMeans

        n_clusters = min(3, len(features) // 5)
        if n_clusters < 2:
            n_clusters = 2

        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(features)

        # Train a random forest to predict the clusters
        model = RandomForestClassifier(n_estimators=50, random_state=42)
        model.fit(features, clusters)

        # Get feature importance
        importances = model.feature_importances_

        # Create DataFrame with results
        importance_df = pd.DataFrame(
            {"feature": feature_names, "importance": importances}
        )

        return importance_df.sort_values("importance", ascending=False).head(n_top)

    @staticmethod
    def get_aggregated_statistics(include_only_with_consent=True):
        """
        Get anonymized, aggregated statistics about the patient population.
        Complies with GDPR by only returning group-level insights.

        Returns:
            dict: Aggregated patient statistics
        """
        from patients.models import Patient
        from campaigns.models import CommunicationLog
        from django.db.models import Avg, Count, Q

        # Only include active patients with consent if required
        patients = Patient.objects.filter(is_active=True)
        if include_only_with_consent:
            patients = patients.filter(has_active_consent=True)

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

        # Language preferences
        language_distribution = dict(
            patients.values("language_preference")
            .annotate(count=Count("id"))
            .values_list("language_preference", "count")
        )

        # Engagement metrics
        avg_engagement = (
            patients.aggregate(avg_score=Avg("engagement_score"))["avg_score"] or 0
        )

        # Communication data
        all_comms = CommunicationLog.objects.filter(patient__in=patients)

        comm_stats = all_comms.aggregate(
            total=Count("id"),
            responded=Count("id", filter=Q(status="RESPONDED")),
            read=Count("id", filter=Q(status="READ")),
            delivered=Count("id", filter=Q(status="DELIVERED")),
        )

        # Communication channel effectiveness
        channel_effectiveness = {}
        for channel in ["EMAIL", "SMS"]:
            channel_logs = all_comms.filter(communication_type=channel)
            channel_count = channel_logs.count()

            if channel_count > 0:
                response_count = channel_logs.filter(status="RESPONDED").count()
                read_count = channel_logs.filter(status="READ").count()

                channel_effectiveness[channel] = {
                    "count": channel_count,
                    "response_rate": response_count / channel_count,
                    "read_rate": read_count / channel_count
                    if channel == "EMAIL"
                    else None,
                }

        # Return the aggregated statistics
        return {
            "status": "success",
            "total_patients": total_count,
            "demographics": {
                "gender": gender_distribution,
                "age_group": age_distribution,
                "location": location_distribution,
            },
            "preferences": {
                "contact_method": contact_method_distribution,
                "language": language_distribution,
            },
            "engagement": {
                "average_score": avg_engagement,
                "response_rate": comm_stats["responded"] / max(1, comm_stats["total"]),
                "delivery_rate": comm_stats["delivered"] / max(1, comm_stats["total"]),
                "read_rate": comm_stats["read"] / max(1, comm_stats["delivered"]),
            },
            "channel_effectiveness": channel_effectiveness,
            "time_period": f"All time as of {timezone.now().strftime('%Y-%m-%d')}",
        }
