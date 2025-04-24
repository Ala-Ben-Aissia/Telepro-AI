"""
Module for training machine learning models for patient response prediction
and campaign effectiveness. Contains the complete pipeline from data extraction
to model training, evaluation, and persistence.
"""

import os
import logging
import joblib
import numpy as np
import pandas as pd
from datetime import timedelta
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from django.utils import timezone

from campaigns.models import CommunicationLog

logger = logging.getLogger(__name__)


class PatientResponseTrainer:
    """
    Trains a machine learning model to predict patient responses to campaigns.
    Uses historical communication logs to build a binary classifier.
    """

    def __init__(self, model_dir="models"):
        """Initialize the trainer with a directory to save models."""
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
        self.model_path = os.path.join(model_dir, "patient_response_model.joblib")

    def generate_training_data(self, lookback_days=365):
        """
        Generate training data from historical communication logs.

        Args:
            lookback_days: Number of days to look back for historical data

        Returns:
            X: Feature matrix
            y: Target vector (1 for response, 0 for no response)
            feature_names: List of feature names
        """
        logger.info(f"Generating training data from the last {lookback_days} days")

        # Get historical communication logs
        cutoff_date = timezone.now() - timedelta(days=lookback_days)
        comm_logs = CommunicationLog.objects.filter(
            sent_at__gte=cutoff_date,
            status__in=["RESPONDED", "READ", "DELIVERED", "SENT"],  # Skip pending/failed
        ).select_related("patient", "campaign")

        if comm_logs.count() == 0:
            logger.error("No historical communication data found for training")
            return None, None, None

        # Prepare data structures
        data = []
        labels = []
        patient_campaigns = set()  # To avoid duplicates

        for log in comm_logs:
            # Skip if we've already processed this patient-campaign combination
            patient_campaign_key = (log.patient.id, log.campaign.id)
            if patient_campaign_key in patient_campaigns:
                continue

            patient_campaigns.add(patient_campaign_key)

            # Extract patient features
            patient = log.patient
            campaign = log.campaign

            # 1. Patient demographic features
            features = {
                "age_group": patient.age_group,
                "gender": patient.gender,
                "language_preference": patient.language_preference,
                "location": patient.location,
                "preferred_contact_method": patient.preferred_contact_method,
            }

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
            features.update(self._extract_historical_features(patient, cutoff_date))

            # Create label (1 if responded, 0 otherwise)
            responded = log.status == "RESPONDED"

            # Add to datasets
            data.append(features)
            labels.append(1 if responded else 0)

        # Convert to DataFrame
        df = pd.DataFrame(data)

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

        # Get feature names
        feature_names = df_encoded.columns.tolist()

        logger.info(
            f"Generated training data with {len(df_encoded)} samples and {len(feature_names)} features"
        )

        return df_encoded.values, np.array(labels), feature_names

    def _extract_historical_features(self, patient, cutoff_date):
        """Extract features from patient's historical activity."""
        features = {}

        # Days since last activity
        if (
            patient.last_campaign_response
            and patient.last_campaign_response >= cutoff_date
        ):
            days_since_response = (timezone.now() - patient.last_campaign_response).days
            features["days_since_response"] = min(days_since_response, 365)
            features["has_recent_response"] = 1
        else:
            features["days_since_response"] = 365  # Default to maximum
            features["has_recent_response"] = 0

        if patient.last_contacted_at and patient.last_contacted_at >= cutoff_date:
            days_since_contact = (timezone.now() - patient.last_contacted_at).days
            features["days_since_contact"] = min(days_since_contact, 365)
            features["has_recent_contact"] = 1
        else:
            features["days_since_contact"] = 365
            features["has_recent_contact"] = 0

        return features

    def train_model(self, classifier="random_forest", test_size=0.2, random_state=42):
        """
        Train a machine learning model to predict patient responses.

        Args:
            classifier: Type of classifier to use ('random_forest' or 'gradient_boosting')
            test_size: Proportion of data to use for testing
            random_state: Random seed for reproducibility

        Returns:
            Dictionary with training results and evaluation metrics
        """
        # Generate training data
        X, y, feature_names = self.generate_training_data()

        if X is None or len(X) < 50:  # Need sufficient data
            return {"status": "error", "message": "Insufficient training data available"}

        # Split into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )

        # Choose classifier
        if classifier == "gradient_boosting":
            clf = GradientBoostingClassifier(random_state=random_state)
        else:  # Default to random forest
            clf = RandomForestClassifier(random_state=random_state)

        # Create pipeline with preprocessing
        pipeline = Pipeline([("scaler", StandardScaler()), ("classifier", clf)])

        # Train model
        logger.info(f"Training {classifier} model with {len(X_train)} samples")
        pipeline.fit(X_train, y_train)

        # Evaluate on test set
        y_pred = pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        # Get probabilities for ROC-AUC
        y_prob = pipeline.predict_proba(X_test)[:, 1]
        roc_auc = roc_auc_score(y_test, y_prob)

        # Cross-validation
        cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring="accuracy")

        # Get feature importance
        if hasattr(pipeline["classifier"], "feature_importances_"):
            importances = pipeline["classifier"].feature_importances_
            feature_importance = dict(zip(feature_names, importances))
            top_features = sorted(
                feature_importance.items(), key=lambda x: x[1], reverse=True
            )[:10]
        else:
            top_features = []

        # Save model
        joblib.dump(pipeline, self.model_path)
        logger.info(f"Model saved to {self.model_path}")

        # Return results
        return {
            "status": "success",
            "model_type": classifier,
            "accuracy": float(accuracy),
            "roc_auc": float(roc_auc),
            "cv_accuracy_mean": float(cv_scores.mean()),
            "cv_accuracy_std": float(cv_scores.std()),
            "model_path": self.model_path,
            "feature_names": feature_names,
            "top_features": top_features,
            "samples_count": len(X),
            "positive_samples": int(y.sum()),
            "training_date": timezone.now().isoformat(),
        }

    def load_model(self):
        """Load the trained model from disk."""
        if not os.path.exists(self.model_path):
            logger.error(f"Model file not found: {self.model_path}")
            return None

        try:
            model = joblib.load(self.model_path)
            logger.info(f"Loaded model from {self.model_path}")
            return model
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return None


# Training function that can be called from the command line or other services
def train_patient_response_model(save_dir="models", classifier="random_forest"):
    """Train and save a patient response prediction model."""
    trainer = PatientResponseTrainer(model_dir=save_dir)
    result = trainer.train_model(classifier=classifier)
    return result
