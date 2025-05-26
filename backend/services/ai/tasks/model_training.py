import logging
import os
from datetime import datetime

from celery import shared_task
from django.utils import timezone

from services.ai.training import train_patient_response_model, PatientResponseTrainer
from services.ai.preprocessing import prepare_data_for_training

logger = logging.getLogger(__name__)


@shared_task(
    name="services.ai.tasks.retrain_patient_response_model",
    bind=True,
    max_retries=2,
    default_retry_delay=600,  # 10 minutes
    time_limit=3600,  # 1 hour time limit
)
def retrain_patient_response_model(
    self,
    save_dir="models",
    classifier="random_forest",
    tune_hyperparameters=True,
    use_smote=True,
    use_feature_selection=False,
    use_ensemble=False,
    ensemble_type="stacking",
):
    """
    Asynchronously train and save a patient response prediction model.

    This is a resource-intensive task that should be scheduled periodically
    to keep the model up to date with the latest patient data.

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
    try:
        logger.info(
            f"Starting model training with {classifier} classifier, "
            f"hyperparameter tuning: {tune_hyperparameters}, "
            f"SMOTE: {use_smote}, feature selection: {use_feature_selection}"
        )

        # Ensure model directory exists
        os.makedirs(save_dir, exist_ok=True)

        # Train the model
        start_time = datetime.now()
        result = train_patient_response_model(
            save_dir=save_dir,
            classifier=classifier,
            tune_hyperparameters=tune_hyperparameters,
            use_smote=use_smote,
            use_feature_selection=use_feature_selection,
            use_ensemble=use_ensemble,
            ensemble_type=ensemble_type,
        )

        training_time = (datetime.now() - start_time).total_seconds()

        # Log training results
        logger.info(
            f"Model training completed in {training_time:.1f} seconds. "
            f"Accuracy: {result.get('accuracy', 0):.4f}, "
            f"F1 Score: {result.get('f1_score', 0):.4f}"
        )

        # Store model metadata
        model_path = os.path.join(save_dir, "model_metadata.json")
        metadata = {
            "trained_at": timezone.now().isoformat(),
            "training_time_seconds": training_time,
            "classifier": classifier,
            "hyperparameter_tuning": tune_hyperparameters,
            "use_smote": use_smote,
            "use_feature_selection": use_feature_selection,
            "use_ensemble": use_ensemble,
            "ensemble_type": ensemble_type if use_ensemble else None,
            "performance": {
                "accuracy": result.get("accuracy", 0),
                "precision": result.get("precision", 0),
                "recall": result.get("recall", 0),
                "f1_score": result.get("f1_score", 0),
                "roc_auc": result.get("roc_auc", 0),
            },
        }

        # In a real implementation, you would save this metadata
        # For example: with open(model_path, 'w') as f: json.dump(metadata, f)

        return {
            "status": "success",
            "training_time_seconds": training_time,
            "performance_metrics": metadata["performance"],
            "model_path": os.path.join(
                save_dir, result.get("model_filename", "model.pkl")
            ),
        }

    except Exception as exc:
        logger.error(f"Error in model training: {str(exc)}")
        if self.request.retries < self.max_retries:
            logger.info(f"Retrying model training (attempt {self.request.retries + 1})")
            self.retry(exc=exc)
        else:
            logger.error("Max retries reached for model training, giving up")
            raise


@shared_task(
    name="services.ai.tasks.evaluate_model_performance",
    bind=True,
    max_retries=2,
    default_retry_delay=300,  # 5 minutes
)
def evaluate_model_performance(self, model_dir="models", test_size=0.2):
    """
    Evaluate the performance of the current production model on recent data.

    This task is useful for detecting model drift and determining if retraining is needed.

    Args:
        model_dir: Directory where the model is stored
        test_size: Proportion of data to use for testing

    Returns:
        Dictionary with evaluation metrics
    """
    try:
        logger.info(f"Evaluating model performance with test_size={test_size}")

        # Create trainer instance
        trainer = PatientResponseTrainer(model_dir=model_dir)

        # Load the existing model
        model, preprocessor = trainer.load_model()

        if not model:
            logger.error("Failed to load model for evaluation")
            return {"status": "error", "message": "Model not found or invalid"}

        # Generate evaluation data
        # In a real implementation, you would load and preprocess recent data
        X_train, X_test, y_train, y_test = prepare_data_for_training(test_size=test_size)

        # Evaluate on test data
        from sklearn.metrics import (
            accuracy_score,
            precision_score,
            recall_score,
            f1_score,
            roc_auc_score,
        )

        # Apply same preprocessing as during training
        X_test_processed = preprocessor.transform(X_test)

        # Make predictions
        y_pred = model.predict(X_test_processed)
        y_pred_proba = (
            model.predict_proba(X_test_processed)[:, 1]
            if hasattr(model, "predict_proba")
            else None
        )

        # Calculate metrics
        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, zero_division=0),
            "recall": recall_score(y_test, y_pred, zero_division=0),
            "f1_score": f1_score(y_test, y_pred, zero_division=0),
        }

        if y_pred_proba is not None:
            metrics["roc_auc"] = roc_auc_score(y_test, y_pred_proba)

        logger.info(
            f"Model evaluation completed. Accuracy: {metrics['accuracy']:.4f}, "
            f"F1 Score: {metrics['f1_score']:.4f}"
        )

        # Store evaluation results
        evaluation_results = {
            "evaluated_at": timezone.now().isoformat(),
            "metrics": metrics,
            "test_size": test_size,
            "test_samples": len(y_test),
        }

        # Determine if model needs retraining based on performance drop
        # In a real implementation, you would compare against previous performance
        needs_retraining = metrics["f1_score"] < 0.7  # Example threshold

        return {
            "status": "success",
            "metrics": metrics,
            "needs_retraining": needs_retraining,
            "evaluation_time": timezone.now().isoformat(),
        }

    except Exception as exc:
        logger.error(f"Error in model evaluation: {str(exc)}")
        if self.request.retries < self.max_retries:
            logger.info(f"Retrying model evaluation (attempt {self.request.retries + 1})")
            self.retry(exc=exc)
        else:
            logger.error("Max retries reached for model evaluation, giving up")
            raise


@shared_task(
    name="services.ai.tasks.compare_model_versions",
    bind=True,
    max_retries=2,
    default_retry_delay=300,  # 5 minutes
)
def compare_model_versions(self, new_model_dir, production_model_dir, test_size=0.3):
    """
    Compare a newly trained model against the production model to determine if it should be deployed.

    Args:
        new_model_dir: Directory containing the new model
        production_model_dir: Directory containing the current production model
        test_size: Proportion of data to use for testing

    Returns:
        Dictionary with comparison results and deployment recommendation
    """
    try:
        logger.info(f"Comparing model versions: new vs production")

        # In a real implementation, you would:
        # 1. Load both models
        # 2. Generate a test dataset
        # 3. Evaluate both models on the same test data
        # 4. Compare performance metrics
        # 5. Make a deployment recommendation

        # This is a placeholder implementation
        new_model_metrics = {
            "accuracy": 0.82,
            "precision": 0.79,
            "recall": 0.77,
            "f1_score": 0.78,
        }

        production_model_metrics = {
            "accuracy": 0.80,
            "precision": 0.76,
            "recall": 0.75,
            "f1_score": 0.75,
        }

        # Determine if new model is better
        improvement = new_model_metrics["f1_score"] - production_model_metrics["f1_score"]
        significant_improvement = improvement > 0.02  # 2% improvement threshold

        logger.info(
            f"Model comparison completed. New model F1: {new_model_metrics['f1_score']:.4f}, "
            f"Production model F1: {production_model_metrics['f1_score']:.4f}, "
            f"Improvement: {improvement:.4f}"
        )

        return {
            "status": "success",
            "new_model_metrics": new_model_metrics,
            "production_model_metrics": production_model_metrics,
            "improvement": {
                "f1_score": improvement,
                "is_significant": significant_improvement,
            },
            "deploy_recommendation": significant_improvement,
        }

    except Exception as exc:
        logger.error(f"Error in model comparison: {str(exc)}")
        if self.request.retries < self.max_retries:
            self.retry(exc=exc)
        else:
            logger.error("Max retries reached for model comparison, giving up")
            raise
