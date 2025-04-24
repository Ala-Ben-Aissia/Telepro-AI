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
            default="random_forest",
            choices=["random_forest", "gradient_boosting"],
            help="Classifier algorithm to use",
        )

    def handle(self, *args, **options):
        model_dir = options["model_dir"]
        classifier = options["classifier"]

        self.stdout.write(
            self.style.HTTP_INFO(f"Training patient response model using {classifier}...")
        )

        result = train_patient_response_model(save_dir=model_dir, classifier=classifier)

        if result["status"] == "success":
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully trained model with accuracy: {result['accuracy']:.2f}, "
                    f"ROC-AUC: {result['roc_auc']:.2f}"
                )
            )
            self.stdout.write(f"Model saved to: {result['model_path']}")

            self.stdout.write("\nTop influential features:")
            for feature, importance in result["top_features"]:
                self.stdout.write(f"  - {feature}: {importance:.4f}")
        else:
            self.stdout.write(
                self.style.ERROR(
                    f"Failed to train model: {result.get('message', 'Unknown error')}"
                )
            )
