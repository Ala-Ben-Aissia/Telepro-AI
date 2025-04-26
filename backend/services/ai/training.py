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
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (
    train_test_split,
    GridSearchCV,
    StratifiedKFold,
    RepeatedStratifiedKFold,
)
from sklearn.base import clone
from sklearn.experimental import enable_halving_search_cv  # Required import
from sklearn.model_selection import HalvingRandomSearchCV
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    StackingClassifier,
    VotingClassifier,
    ExtraTreesClassifier,
)
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
from sklearn.feature_selection import SelectFromModel

from campaigns.models import CommunicationLog
from .preprocessing import calculate_response_trend  # Add this import

logger = logging.getLogger(__name__)


def create_ensemble_model(model_type="stacking"):
    """
    Create an ensemble model with advanced configuration and learning rate scheduling.
    """
    # Base classifiers with optimized hyperparameters
    rf = RandomForestClassifier(
        n_estimators=1000,  # Increased for better convergence
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        class_weight="balanced",
        bootstrap=True,
        max_features="sqrt",
        n_jobs=-1,  # Utilize all cores
    )

    gb = GradientBoostingClassifier(
        n_estimators=500,  # Increased from 300
        learning_rate=0.01,
        max_depth=6,
        subsample=0.8,
        max_features="sqrt",
        random_state=42,
        validation_fraction=0.2,  # Increased validation set
        n_iter_no_change=20,  # More patience
        tol=1e-5,  # Stricter convergence
    )

    et = ExtraTreesClassifier(
        n_estimators=500,
        max_depth=15,
        min_samples_split=4,
        random_state=42,
        class_weight="balanced",
        bootstrap=True,
        max_features="sqrt",
        n_jobs=-1,
    )

    if model_type == "voting":
        ensemble = VotingClassifier(
            estimators=[("rf", rf), ("gb", gb), ("et", et)],
            voting="soft",
            weights=[1, 2, 1],
        )
    else:
        meta_classifier = LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
            random_state=42,
            C=0.1,
            solver="saga",
            penalty="l2",  # Changed from elasticnet since saga doesn't support it
            n_jobs=-1,
        )

        # Use simple StratifiedKFold instead of RepeatedStratifiedKFold
        ensemble = StackingClassifier(
            estimators=[("rf", rf), ("gb", gb), ("et", et)],
            final_estimator=meta_classifier,
            cv=5,  # Simple k-fold CV
            passthrough=True,
            n_jobs=-1,
        )

    return ensemble


def select_optimal_features(X, y, threshold="median"):
    """
    Select most important features using Random Forest feature importance.
    Returns a fitted selector. Use selector.transform(X) to get reduced features.
    """
    selector = SelectFromModel(
        RandomForestClassifier(n_estimators=100, random_state=42), threshold=threshold
    )
    selector.fit(X, y)
    return selector


# Example usage in training pipeline:
# selector = select_optimal_features(X_train, y_train)
# X_train_selected = selector.transform(X_train)
# X_test_selected = selector.transform(X_test)
# selected_features = [f for f, s in zip(feature_names, selector.get_support()) if s]


class PatientResponseTrainer:
    """
    Trains a machine learning model to predict patient responses to campaigns.
    Uses historical communication logs to build a binary classifier.
    """

    def __init__(self, model_dir="models"):
        """Initialize the trainer with a directory to save models."""
        self.model_dir = model_dir
        self.use_smote = True  # Default value
        os.makedirs(model_dir, exist_ok=True)
        self.model_path = os.path.join(model_dir, "patient_response_model.joblib")
        self.metrics_path = os.path.join(model_dir, "patient_response_model_metrics.png")

    def generate_training_data(self, lookback_days=720):
        """
        Generate training data from historical communication logs.
        Now includes aggregated historical interactions and temporal patterns.
        """
        logger.info(f"Generating training data from the last {lookback_days} days")

        cutoff_date = timezone.now() - timedelta(days=lookback_days)
        comm_logs = CommunicationLog.objects.filter(
            sent_at__gte=cutoff_date,
            status__in=["RESPONDED", "READ", "DELIVERED", "SENT"],
        ).select_related("patient", "campaign")

        total_logs = comm_logs.count()
        if total_logs == 0:
            logger.error("No historical communication data found for training")
            return None, None, None

        logger.info(f"Found {total_logs} communication logs for model training")

        # Group logs by patient for historical pattern analysis
        patient_history = {}
        for log in comm_logs:
            if log.patient_id not in patient_history:
                patient_history[log.patient_id] = []
            patient_history[log.patient_id].append(log)

        # Prepare data structures
        data = []
        labels = []

        # Process each communication log with enhanced features
        for log in comm_logs:
            try:
                patient = log.patient
                campaign = log.campaign
                patient_logs = sorted(
                    patient_history[patient.id], key=lambda x: x.sent_at or timezone.now()
                )

                # 1. Enhanced Patient demographic features
                features = {
                    "age_group": patient.age_group or "Unknown",
                    "gender": patient.gender or "Unknown",
                    "language_preference": patient.language_preference or "Unknown",
                    "location": patient.location or "Unknown",
                    "preferred_contact_method": patient.preferred_contact_method,
                }

                # 2. Enhanced engagement metrics with historical patterns
                recent_responses = sum(
                    1 for l in patient_logs[-5:] if l.status == "RESPONDED"
                )
                response_trend = calculate_response_trend(patient)

                features.update(
                    {
                        "engagement_score": float(patient.engagement_score),
                        "contact_attempts": min(patient.contact_attempts, 50),
                        "successful_contacts": min(patient.successful_contacts, 50),
                        "contact_success_rate": patient.successful_contacts
                        / max(1, patient.contact_attempts),
                        "email_verified": int(patient.email_verified),
                        "phone_verified": int(patient.phone_verified),
                        "recent_response_rate": recent_responses / 5.0,
                        "response_trend": response_trend,
                    }
                )

                # 3. Enhanced campaign features with content analysis
                email_len = len(campaign.email_template) if campaign.email_template else 0
                sms_len = len(campaign.sms_template) if campaign.sms_template else 0

                features.update(
                    {
                        "campaign_category": campaign.category.name
                        if campaign.category
                        else "Unknown",
                        "has_email_template": 1 if campaign.email_template else 0,
                        "has_sms_template": 1 if campaign.sms_template else 0,
                        "email_template_length": email_len,
                        "sms_template_length": sms_len,
                        "total_content_length": email_len + sms_len,
                    }
                )

                # 4. Enhanced matching features with weighted scores
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

                # Calculate weighted match score with more emphasis on language and location
                match_score = (
                    (0.3 if matches_age_group else 0)  # Reduced weight for age group
                    + (0.4 if matches_location else 0)  # Increased weight for location
                    + (0.3 if matches_language else 0)  # Kept same weight for language
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

                # 5. Enhanced historical features with temporal patterns
                historical_features = self._extract_historical_features(
                    patient, cutoff_date
                )
                features.update(historical_features)

                # 6. Enhanced communication context features
                if log.sent_at:
                    hour = log.sent_at.hour
                    features.update(
                        {
                            "sent_hour": hour,
                            "sent_day_of_week": log.sent_at.weekday(),
                            "sent_month": log.sent_at.month,
                            "is_business_hours": 1 if 9 <= hour <= 17 else 0,
                            "is_evening": 1 if 17 <= hour <= 21 else 0,
                            "is_weekend": 1 if log.sent_at.weekday() >= 5 else 0,
                        }
                    )
                else:
                    features.update(
                        {
                            "sent_hour": 12,
                            "sent_day_of_week": 2,
                            "sent_month": 6,
                            "is_business_hours": 1,
                            "is_evening": 0,
                            "is_weekend": 0,
                        }
                    )

                # 7. Response pattern features
                prev_logs = [
                    l for l in patient_logs if l.sent_at and l.sent_at < log.sent_at
                ]
                if prev_logs:
                    last_response = next(
                        (l for l in reversed(prev_logs) if l.status == "RESPONDED"), None
                    )
                    if last_response:
                        days_since_last_response = (
                            log.sent_at - last_response.sent_at
                        ).days
                        features["days_since_last_response"] = min(
                            days_since_last_response, 365
                        )
                        features["had_previous_response"] = 1
                    else:
                        features["days_since_last_response"] = 365
                        features["had_previous_response"] = 0
                else:
                    features["days_since_last_response"] = 365
                    features["had_previous_response"] = 0

                # Create label (1 if responded, 0 otherwise)
                responded = log.status == "RESPONDED"

                # Add to datasets only if the features are complete
                if all(v is not None for v in features.values()):
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

        # Log feature correlations with target
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
        """Enhanced hyperparameter tuning using Halving Random Search"""
        logger.info(f"Performing hyperparameter tuning for {classifier_type}")

        if classifier_type == "gradient_boosting":
            param_distributions = {
                "classifier__n_estimators": [100, 200, 300, 500],
                "classifier__learning_rate": [0.001, 0.01, 0.05, 0.1],
                "classifier__max_depth": [3, 4, 5, 6, 7],
                "classifier__min_samples_split": [2, 5, 10],
                "classifier__subsample": [0.6, 0.7, 0.8, 0.9],
                "classifier__max_features": ["sqrt", "log2"],
                "classifier__validation_fraction": [0.1, 0.2],
                "classifier__n_iter_no_change": [10, 20, 30],
                "classifier__tol": [1e-5, 1e-4, 1e-3],
            }
            base_clf = GradientBoostingClassifier(random_state=42)
        else:
            param_distributions = {
                "classifier__n_estimators": [100, 300, 500, 1000],
                "classifier__max_depth": [10, 15, 20, 25, None],
                "classifier__min_samples_split": [2, 4, 5, 10],
                "classifier__min_samples_leaf": [1, 2, 4],
                "classifier__max_features": ["sqrt", "log2"],
                "classifier__bootstrap": [True, False],
            }
            base_clf = RandomForestClassifier(
                random_state=42, class_weight="balanced" if not self.use_smote else None
            )

        pipeline = Pipeline([("scaler", StandardScaler()), ("classifier", base_clf)])

        # Use repeated stratified k-fold
        cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=42)

        # Use Halving Random Search with single scoring metric
        search = HalvingRandomSearchCV(
            pipeline,
            param_distributions,
            cv=cv,
            factor=2,
            n_candidates=20,  # Number of parameter settings that are sampled
            min_resources=20,  # Minimum number of samples used
            scoring="roc_auc",  # Use ROC-AUC as primary metric
            n_jobs=-1,
            random_state=42,
            verbose=1,
        )

        search.fit(X, y)

        logger.info(f"Best parameters: {search.best_params_}")
        logger.info(f"Best ROC-AUC score: {search.best_score_:.4f}")

        # Additional scoring metrics using cross_val_score
        from sklearn.model_selection import cross_val_score

        best_pipeline = Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    clone(base_clf).set_params(
                        **{
                            k.replace("classifier__", ""): v
                            for k, v in search.best_params_.items()
                        }
                    ),
                ),
            ]
        )

        for metric in ["average_precision", "f1"]:
            scores = cross_val_score(best_pipeline, X, y, cv=cv, scoring=metric)
            logger.info(
                f"{metric} score: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})"
            )

        return search.best_params_

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
        use_feature_selection=False,
        use_ensemble=False,
        ensemble_type="stacking",
    ):
        """Train a machine learning model to predict patient responses."""
        # Generate training data
        X, y, feature_names = self.generate_training_data()

        if X is None or len(X) < 50:
            logger.error("Insufficient training data")
            return {"status": "error", "message": "Insufficient training data available"}

        # Handle missing values and normalize features
        from sklearn.impute import SimpleImputer

        imputer = SimpleImputer(strategy="median")
        X = imputer.fit_transform(X)

        # Feature selection (optional)
        selector = None
        if use_feature_selection:
            selector = select_optimal_features(X, y)
            X = selector.transform(X)
            feature_names = [
                f for f, s in zip(feature_names, selector.get_support()) if s
            ]

        # Ensure we have enough samples of each class before splitting
        unique_classes = np.unique(y)
        if len(unique_classes) < 2:
            logger.error("Need samples from at least 2 classes")
            return {
                "status": "error",
                "message": "Insufficient class diversity in training data",
            }

        # Split into training and testing sets with stratification
        stratified_splitter = StratifiedKFold(
            n_splits=5, shuffle=True, random_state=random_state
        )
        train_idx, test_idx = next(stratified_splitter.split(X, y))

        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        # Handle class imbalance if needed
        class_counts = np.bincount(y_train)
        if use_smote and (min(class_counts) / max(class_counts) < 0.5):
            logger.info("Applying SMOTE for class imbalance")
            try:
                smote = SMOTE(
                    random_state=random_state,
                    sampling_strategy="auto",
                    k_neighbors=min(5, min(class_counts) - 1),
                )
                X_train, y_train = smote.fit_resample(X_train, y_train)
                logger.info(f"After SMOTE - training samples: {len(X_train)}")
            except Exception as e:
                logger.warning(f"SMOTE failed, proceeding without it: {str(e)}")
                use_smote = False

        # Choose and configure classifier
        if use_ensemble:
            logger.info(f"Creating ensemble model with {ensemble_type} strategy")
            clf = create_ensemble_model(model_type=ensemble_type)
        elif classifier == "gradient_boosting":
            clf = GradientBoostingClassifier(
                random_state=random_state,
                n_estimators=100,
                learning_rate=0.1,
                max_depth=3,
                validation_fraction=0.2,
            )
        else:
            clf = RandomForestClassifier(
                n_estimators=100,
                max_depth=None,
                random_state=random_state,
                class_weight="balanced" if not use_smote else None,
                min_samples_leaf=2,
            )

        # Perform hyperparameter tuning if requested
        best_params = None
        if tune_hyperparameters:
            logger.info("Performing hyperparameter tuning")
            best_params = self._tune_hyperparameters(X_train, y_train, classifier)
            if best_params:
                for param, value in best_params.items():
                    param_name = param.replace("classifier__", "")
                    if hasattr(clf, param_name):
                        setattr(clf, param_name, value)

        # Create and train pipeline
        logger.info(f"Training {classifier} model with {len(X_train)} samples")
        pipeline = Pipeline([("scaler", StandardScaler()), ("classifier", clf)])

        # Fit with error handling
        try:
            pipeline.fit(X_train, y_train)
        except Exception as e:
            logger.error(f"Model training failed: {str(e)}")
            return {"status": "error", "message": f"Model training failed: {str(e)}"}

        # Evaluate
        try:
            y_pred = pipeline.predict(X_test)
            y_prob = pipeline.predict_proba(X_test)[:, 1]

            # Calculate metrics
            accuracy = accuracy_score(y_test, y_pred)
            roc_auc = roc_auc_score(y_test, y_prob)
            avg_precision = average_precision_score(y_test, y_prob)
            class_report = classification_report(y_test, y_pred, output_dict=True)

            # Plot metrics and learning curves
            self._plot_metrics(y_test, y_pred, y_prob)
            self._plot_learning_curves(X, y, pipeline)

        except Exception as e:
            logger.error(f"Error during model evaluation: {str(e)}")
            return {"status": "error", "message": f"Model evaluation failed: {str(e)}"}

        # Get feature importance
        top_features = {}
        if hasattr(pipeline["classifier"], "feature_importances_"):
            try:
                importances = pipeline["classifier"].feature_importances_
                indices = np.argsort(importances)[::-1]
                top_features = {
                    feature_names[i]: float(importances[i]) for i in indices[:10]
                }
                logger.info("Top influential features:")
                for feat, imp in top_features.items():
                    logger.info(f"  - {feat}: {imp:.4f}")
            except Exception as e:
                logger.warning(f"Could not extract feature importances: {str(e)}")

        # Save model and return results
        try:
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
                "feature_selector": selector if use_feature_selection else None,
            }
            joblib.dump(model_data, self.model_path)
            logger.info(f"Model saved to {self.model_path}")
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            return {"status": "error", "message": f"Could not save model: {str(e)}"}

        return {
            "status": "success",
            "model_type": classifier,
            "accuracy": float(accuracy),
            "roc_auc": float(roc_auc),
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
            "feature_selection": use_feature_selection,
            "selected_feature_count": len(feature_names)
            if use_feature_selection
            else None,
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
    classifier="random_forest",  # Can also be 'gradient_boosting' or 'ensemble'
    tune_hyperparameters=True,
    use_smote=True,
    use_feature_selection=False,
    use_ensemble=False,
    ensemble_type="stacking",
):
    """
    Train and save a patient response prediction model.

    Args:
        save_dir: Directory to save the model
        classifier: Base classifier type ("random_forest", "gradient_boosting", or "ensemble")
        tune_hyperparameters: Whether to perform hyperparameter tuning
        use_smote: Whether to apply SMOTE for class imbalance
        use_feature_selection: Whether to select important features before training
        use_ensemble: Whether to use an ensemble of models
        ensemble_type: Type of ensemble to use ("stacking" or "voting")

    Returns:
        Dictionary with training results
    """
    trainer = PatientResponseTrainer(model_dir=save_dir)
    result = trainer.train_model(
        classifier=classifier,
        tune_hyperparameters=tune_hyperparameters,
        use_smote=use_smote,
        use_feature_selection=use_feature_selection,
        use_ensemble=use_ensemble,
        ensemble_type=ensemble_type,
    )
    return result
