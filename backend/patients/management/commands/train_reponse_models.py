from django.core.management.base import BaseCommand
from services.ai.training import train_patient_response_model


class Command(BaseCommand):
    help = "Train a machine learning model to predict patient responses to campaigns"

    def add_arguments(self, parser):
        parser.add_argument(
            "--model-dir",
            type=str,
            default="models",
            help="Directory to save the trained model",
        )
        parser.add_argument(
            "--classifier",
            type=str,
            default="ensemble",  # Changed default to ensemble
            choices=["random_forest", "gradient_boosting", "ensemble"],
            help="Classifier algorithm to use",
        )
        parser.add_argument(
            "--tune",
            action="store_true",
            help="Perform hyperparameter tuning",
        )
        parser.add_argument(
            "--smote",
            action="store_true",
            default=True,  # Enable SMOTE by default
            help="Use SMOTE for class imbalance",
        )

    def handle(self, *args, **options):
        model_dir = options["model_dir"]
        classifier = options["classifier"]
        tune_hyperparameters = options["tune"]
        use_smote = options["smote"]

        self.stdout.write(
            self.style.HTTP_INFO(f"Training patient response model using {classifier}...")
        )

        if tune_hyperparameters:
            self.stdout.write("Hyperparameter tuning enabled (this may take a while)")

        if use_smote:
            self.stdout.write("SMOTE oversampling enabled for handling class imbalance")

        # Use optimized settings
        result = train_patient_response_model(
            save_dir=model_dir,
            classifier=classifier,
            tune_hyperparameters=True,  # Always tune hyperparameters
            use_smote=True,  # Always use SMOTE
            use_feature_selection=True,  # Enable feature selection
            use_ensemble=True,  # Use ensemble methods
            ensemble_type="stacking",  # Use stacking ensemble
        )

        if result["status"] == "success":
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully trained model with accuracy: {result['accuracy']:.2f}, "
                    f"ROC-AUC: {result['roc_auc']:.2f}"
                )
            )

            self.stdout.write(f"Precision: {result['precision']:.2f}")
            self.stdout.write(f"Recall: {result['recall']:.2f}")
            self.stdout.write(f"F1 Score: {result['f1_score']:.2f}")

            # Class distribution
            self.stdout.write(
                f"Class distribution - Positive rate: {result['positive_rate']:.2%}"
            )

            self.stdout.write(f"Model saved to: {result['model_path']}")
            self.stdout.write(f"Metrics visualization: {result['metrics_plot']}")

            self.stdout.write("\nTop influential features:")
            for feature, importance in result["top_features"]:
                self.stdout.write(f"  - {feature}: {importance:.4f}")
        else:
            self.stdout.write(
                self.style.ERROR(
                    f"Failed to train model: {result.get('message', 'Unknown error')}"
                )
            )
