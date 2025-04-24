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
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    classification_report,
    accuracy_score,
    roc_auc_score,
    average_precision_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.utils.class_weight import compute_class_weight
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt
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
        self.metrics_path = os.path.join(model_dir, "patient_response_model_metrics.png")

    def generate_training_data(self, lookback_days=720):  # Extended lookback period
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

        total_logs = comm_logs.count()
        if total_logs == 0:
            logger.error("No historical communication data found for training")
            return None, None, None

        logger.info(f"Found {total_logs} communication logs for model training")

        # Prepare data structures
        data = []
        labels = []
        patient_campaigns = {}  # Store the latest communication for each patient-campaign pair

        # First pass: identify the latest communication for each patient-campaign pair
        for log in comm_logs:
            patient_campaign_key = (str(log.patient.id), log.campaign.id)

            # If we haven't seen this pair before, or this log is newer
            if patient_campaign_key not in patient_campaigns or (
                log.sent_at
                and patient_campaigns[patient_campaign_key].sent_at
                and log.sent_at > patient_campaigns[patient_campaign_key].sent_at
            ):
                patient_campaigns[patient_campaign_key] = log

        # Second pass: process only the latest communication for each patient-campaign pair
        for log in patient_campaigns.values():
            try:
                # Extract patient features
                patient = log.patient
                campaign = log.campaign

                # 1. Patient demographic features
                features = {
                    "age_group": patient.age_group or "Unknown",
                    "gender": patient.gender or "Unknown",
                    "language_preference": patient.language_preference or "Unknown",
                    "location": patient.location or "Unknown",
                    "preferred_contact_method": patient.preferred_contact_method,
                }

                # 2. Patient engagement metrics
                features.update(
                    {
                        "engagement_score": float(patient.engagement_score),
                        "contact_attempts": min(
                            patient.contact_attempts, 50
                        ),  # Cap to avoid outliers
                        "successful_contacts": min(patient.successful_contacts, 50),
                        "contact_success_rate": (
                            patient.successful_contacts / max(1, patient.contact_attempts)
                        ),
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
                        "email_template_length": len(campaign.email_template)
                        if campaign.email_template
                        else 0,
                        "sms_template_length": len(campaign.sms_template)
                        if campaign.sms_template
                        else 0,
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
                    lang == patient.language_preference
                    for lang in campaign.target_languages
                )

                # Calculate a match score (0-1)
                match_score = (
                    (0.4 if matches_age_group else 0)
                    + (0.3 if matches_location else 0)
                    + (0.3 if matches_language else 0)
                )

                features.update(
                    {
                        "matches_age_group": int(matches_age_group),
                        "matches_location": int(matches_location),
                        "matches_language": int(matches_language),
                        "match_score": match_score,
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

                # 6. Communication context features
                if log.sent_at:
                    features["sent_hour"] = log.sent_at.hour
                    features["sent_day_of_week"] = log.sent_at.weekday()
                    features["sent_month"] = log.sent_at.month
                else:
                    # Default values if sent_at is None
                    features["sent_hour"] = 12  # Noon as default
                    features["sent_day_of_week"] = 2  # Wednesday as default
                    features["sent_month"] = 6  # June as default

                # Create label (1 if responded, 0 otherwise)
                responded = log.status == "RESPONDED"

                # Add to datasets
                data.append(features)
                labels.append(1 if responded else 0)

            except Exception as e:
                logger.warning(f"Error processing log {log.id}: {str(e)}")
                continue

        if not data:
            logger.error("No valid data extracted from communication logs")
            return None, None, None

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Check for correlation between features and target
        y_array = np.array(labels)
        for col in df.columns:
            if df[col].dtype in [np.int64, np.float64]:
                corr = np.corrcoef(df[col], y_array)[0, 1]
                logger.info(f"Correlation of {col} with target: {corr:.4f}")

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

        # Check class balance
        positive_rate = np.mean(labels)
        logger.info(
            f"Class distribution - Positive: {positive_rate:.2%}, Negative: {(1 - positive_rate):.2%}"
        )

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
            features["has_recent_response"] = 1 if days_since_response <= 30 else 0
            features["has_very_recent_response"] = 1 if days_since_response <= 7 else 0
        else:
            features["days_since_response"] = 365  # Default to maximum
            features["has_recent_response"] = 0
            features["has_very_recent_response"] = 0

        if patient.last_contacted_at and patient.last_contacted_at >= cutoff_date:
            days_since_contact = (timezone.now() - patient.last_contacted_at).days
            features["days_since_contact"] = min(days_since_contact, 365)
            features["has_recent_contact"] = 1 if days_since_contact <= 30 else 0
            features["has_very_recent_contact"] = 1 if days_since_contact <= 7 else 0
        else:
            features["days_since_contact"] = 365
            features["has_recent_contact"] = 0
            features["has_very_recent_contact"] = 0

        # Additional derived features
        features["contact_frequency"] = patient.contact_attempts / max(
            1, (timezone.now() - patient.created_at).days / 30
        )  # Attempts per month

        return features

    def _tune_hyperparameters(self, X, y, classifier_type):
        """
        Perform hyperparameter tuning using GridSearchCV.

        Args:
            X: Feature matrix
            y: Target vector
            classifier_type: Type of classifier ('random_forest' or 'gradient_boosting')

        Returns:
            Best parameters found
        """
        logger.info(f"Performing hyperparameter tuning for {classifier_type}")

        # Define parameter grid based on classifier type
        if classifier_type == "gradient_boosting":
            param_grid = {
                "classifier__n_estimators": [50, 100, 200],
                "classifier__learning_rate": [0.01, 0.1, 0.2],
                "classifier__max_depth": [3, 5, 7],
                "classifier__min_samples_split": [2, 5, 10],
            }
            base_clf = GradientBoostingClassifier(random_state=42)
        else:  # Random Forest
            param_grid = {
                "classifier__n_estimators": [50, 100, 200],
                "classifier__max_depth": [None, 10, 20],
                "classifier__min_samples_split": [2, 5, 10],
                "classifier__min_samples_leaf": [1, 2, 4],
            }
            base_clf = RandomForestClassifier(random_state=42)

        # Create pipeline with preprocessing
        pipeline = Pipeline([("scaler", StandardScaler()), ("classifier", base_clf)])

        # Set up cross-validation
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

        # Create grid search
        grid_search = GridSearchCV(
            pipeline, param_grid, cv=cv, scoring="roc_auc", n_jobs=-1, verbose=1
        )

        # Fit grid search
        grid_search.fit(X, y)

        logger.info(f"Best parameters: {grid_search.best_params_}")
        logger.info(f"Best score: {grid_search.best_score_:.4f}")

        return grid_search.best_params_

    def _plot_learning_curves(self, X, y, pipeline, cv=5):
        """
        Plot learning curves to diagnose overfitting/underfitting.

        Args:
            X: Feature matrix
            y: Target vector
            pipeline: Trained pipeline
            cv: Number of cross-validation folds
        """
        from sklearn.model_selection import learning_curve

        train_sizes = np.linspace(0.1, 1.0, 10)
        train_sizes, train_scores, test_scores = learning_curve(
            pipeline,
            X,
            y,
            cv=cv,
            train_sizes=train_sizes,
            scoring="accuracy",
            n_jobs=-1,
            random_state=42,
        )

        train_mean = np.mean(train_scores, axis=1)
        train_std = np.std(train_scores, axis=1)
        test_mean = np.mean(test_scores, axis=1)
        test_std = np.std(test_scores, axis=1)

        plt.figure(figsize=(10, 6))
        plt.grid()

        plt.fill_between(
            train_sizes,
            train_mean - train_std,
            train_mean + train_std,
            alpha=0.1,
            color="blue",
        )
        plt.fill_between(
            train_sizes,
            test_mean - test_std,
            test_mean + test_std,
            alpha=0.1,
            color="red",
        )
        plt.plot(train_sizes, train_mean, "o-", color="blue", label="Training score")
        plt.plot(
            train_sizes, test_mean, "o-", color="red", label="Cross-validation score"
        )

        plt.xlabel("Training examples")
        plt.ylabel("Accuracy score")
        plt.title("Learning Curves")
        plt.legend(loc="best")

        curves_path = os.path.join(self.model_dir, "learning_curves.png")
        plt.savefig(curves_path)
        plt.close()

        logger.info(f"Learning curves saved to {curves_path}")

    def _plot_metrics(self, y_test, y_pred, y_prob):
        """
        Plot metrics for model evaluation.

        Args:
            y_test: True labels
            y_pred: Predicted labels
            y_prob: Predicted probabilities for positive class
        """
        from sklearn.metrics import (
            precision_recall_curve,
            roc_curve,
            auc,
            confusion_matrix,
        )
        import matplotlib.pyplot as plt
        import seaborn as sns

        # Create figure with multiple subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))

        # 1. Precision-Recall Curve
        precision, recall, _ = precision_recall_curve(y_test, y_prob)
        avg_precision = average_precision_score(y_test, y_prob)

        axes[0, 0].plot(recall, precision, color="blue", lw=2)
        axes[0, 0].set_xlabel("Recall")
        axes[0, 0].set_ylabel("Precision")
        axes[0, 0].set_title(f"Precision-Recall Curve (AP={avg_precision:.3f})")
        axes[0, 0].grid(True)

        # 2. ROC Curve
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)

        axes[0, 1].plot(fpr, tpr, color="darkorange", lw=2)
        axes[0, 1].plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
        axes[0, 1].set_xlabel("False Positive Rate")
        axes[0, 1].set_ylabel("True Positive Rate")
        axes[0, 1].set_title(f"ROC Curve (AUC={roc_auc:.3f})")
        axes[0, 1].grid(True)

        # 3. Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)

        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=axes[1, 0])
        axes[1, 0].set_xlabel("Predicted")
        axes[1, 0].set_ylabel("True")
        axes[1, 0].set_title("Confusion Matrix")

        # 4. Probability Distribution
        axes[1, 1].hist(
            y_prob[y_test == 0], bins=20, alpha=0.5, label="Negative Class", color="red"
        )
        axes[1, 1].hist(
            y_prob[y_test == 1], bins=20, alpha=0.5, label="Positive Class", color="green"
        )
        axes[1, 1].set_xlabel("Probability of Response")
        axes[1, 1].set_ylabel("Count")
        axes[1, 1].set_title("Probability Distributions")
        axes[1, 1].legend()

        plt.tight_layout()
        plt.savefig(self.metrics_path)
        plt.close()

        logger.info(f"Model metrics visualizations saved to {self.metrics_path}")

    def train_model(
        self,
        classifier="random_forest",
        tune_hyperparameters=True,
        test_size=0.2,
        random_state=42,
        use_smote=True,
    ):
        """
        Train a machine learning model to predict patient responses.

        Args:
            classifier: Type of classifier to use ('random_forest' or 'gradient_boosting')
            tune_hyperparameters: Whether to perform hyperparameter tuning
            test_size: Proportion of data to use for testing
            random_state: Random seed for reproducibility
            use_smote: Whether to use SMOTE for handling class imbalance

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

        # Handle class imbalance if needed
        class_counts = np.bincount(y_train)
        if use_smote and (min(class_counts) / max(class_counts) < 0.5):
            logger.info("Using SMOTE to handle class imbalance")
            try:
                smote = SMOTE(random_state=random_state)
                X_train_resampled, y_train_resampled = smote.fit_resample(
                    X_train, y_train
                )
                logger.info(
                    f"SMOTE applied - Data increased from {len(X_train)} to {len(X_train_resampled)}"
                )
                X_train, y_train = X_train_resampled, y_train_resampled
            except Exception as e:
                logger.warning(f"SMOTE failed, falling back to class weights: {str(e)}")
                use_smote = False

        # Compute class weights if not using SMOTE
        if not use_smote:
            class_weights = compute_class_weight(
                "balanced", classes=np.unique(y_train), y=y_train
            )
            weight_dict = {i: weight for i, weight in enumerate(class_weights)}
            logger.info(f"Using class weights: {weight_dict}")
        else:
            weight_dict = None

        # Choose classifier
        if classifier == "gradient_boosting":
            clf = GradientBoostingClassifier(random_state=random_state)
        else:  # Default to random forest
            clf = RandomForestClassifier(
                random_state=random_state,
                class_weight=weight_dict if not use_smote else None,
            )

        # Perform hyperparameter tuning if requested
        best_params = {}
        if tune_hyperparameters:
            best_params = self._tune_hyperparameters(X_train, y_train, classifier)

            # Update classifier with best parameters
            if classifier == "gradient_boosting":
                clf = GradientBoostingClassifier(
                    random_state=random_state,
                    **{k.replace("classifier__", ""): v for k, v in best_params.items()},
                )
            else:
                clf = RandomForestClassifier(
                    random_state=random_state,
                    class_weight=weight_dict if not use_smote else None,
                    **{k.replace("classifier__", ""): v for k, v in best_params.items()},
                )

        # Create pipeline with preprocessing
        pipeline = Pipeline([("scaler", StandardScaler()), ("classifier", clf)])

        # Train model
        logger.info(f"Training {classifier} model with {len(X_train)} samples")
        pipeline.fit(X_train, y_train)

        # Evaluate on test set
        y_pred = pipeline.predict(X_test)
        y_prob = pipeline.predict_proba(X_test)[:, 1]

        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_prob)
        avg_precision = average_precision_score(y_test, y_prob)
        class_report = classification_report(y_test, y_pred, output_dict=True)

        # Save model visualization
        self._plot_metrics(y_test, y_pred, y_prob)

        # Plot learning curves for diagnosis
        self._plot_learning_curves(X, y, pipeline)

        # Get feature importance
        if hasattr(pipeline["classifier"], "feature_importances_"):
            importances = pipeline["classifier"].feature_importances_
            feature_importance = dict(zip(feature_names, importances))
            top_features = sorted(
                feature_importance.items(), key=lambda x: x[1], reverse=True
            )[:10]
        else:
            top_features = []

        # Save model and feature names
        model_data = {
            "pipeline": pipeline,
            "feature_names": feature_names,
            "training_date": timezone.now().isoformat(),
            "metrics": {
                "accuracy": float(accuracy),
                "roc_auc": float(roc_auc),
                "avg_precision": float(avg_precision),
                "class_report": class_report,
            },
        }
        joblib.dump(model_data, self.model_path)
        logger.info(f"Model saved to {self.model_path}")

        # Return results
        return {
            "status": "success",
            "model_type": classifier,
            "accuracy": float(accuracy),
            "roc_auc": float(roc_auc),
            "avg_precision": float(avg_precision),
            "precision": float(class_report["1"]["precision"]),
            "recall": float(class_report["1"]["recall"]),
            "f1_score": float(class_report["1"]["f1-score"]),
            "model_path": self.model_path,
            "metrics_plot": self.metrics_path,
            "feature_names": feature_names,
            "top_features": top_features,
            "samples_count": len(X),
            "positive_samples": int(y.sum()),
            "positive_rate": float(y.sum() / len(y)),
            "smote_applied": use_smote,
            "hyperparameter_tuning": tune_hyperparameters,
            "best_params": best_params,
            "training_date": timezone.now().isoformat(),
        }

    def load_model(self):
        """Load the trained model from disk."""
        if not os.path.exists(self.model_path):
            logger.error(f"Model file not found: {self.model_path}")
            return None

        try:
            model_data = joblib.load(self.model_path)
            logger.info(f"Loaded model from {self.model_path}")
            return model_data
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return None


def train_patient_response_model(
    save_dir="models",
    classifier="random_forest",
    tune_hyperparameters=True,
    use_smote=True,
):
    """Train and save a patient response prediction model."""
    trainer = PatientResponseTrainer(model_dir=save_dir)
    result = trainer.train_model(
        classifier=classifier,
        tune_hyperparameters=tune_hyperparameters,
        use_smote=use_smote,
    )
    return result
