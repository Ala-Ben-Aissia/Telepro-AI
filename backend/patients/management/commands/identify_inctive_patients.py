from django.core.management.base import BaseCommand
from services.ai.prediction import CampaignPredictionService
from django.core.mail import send_mail
from django.conf import settings
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Identify patients who are at risk of becoming inactive and need follow-up"

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=90,
            help="Days threshold for considering a patient inactive",
        )
        parser.add_argument(
            "--notify",
            action="store_true",
            help="Send email notification to staff with results",
        )
        parser.add_argument(
            "--skip-email",
            action="store_true",
            help="Skip sending email even if --notify is provided (for testing)",
        )
        parser.add_argument(
            "--min-risk",
            type=float,
            default=0.6,
            help="Minimum risk score to include a patient in results",
        )
        parser.add_argument(
            "--output",
            type=str,
            choices=["json", "csv", "console"],
            default="console",
            help="Output format for results",
        )

    def handle(self, *args, **options):
        days_threshold = options["days"]
        min_risk = options["min_risk"]
        output_format = options["output"]
        notify = options["notify"]
        skip_email = options["skip_email"]

        self.stdout.write(
            self.style.HTTP_INFO(
                f"Identifying inactive patients (days threshold: {days_threshold}, risk threshold: {min_risk})..."
            )
        )

        # Get high-risk inactive patients
        results = CampaignPredictionService.predict_inactive_patients(days_threshold)

        # Filter by minimum risk if needed
        filtered_results = [r for r in results if r["risk_score"] >= min_risk]

        # Output results
        self.stdout.write(
            f"Found {len(filtered_results)} patients at risk of becoming inactive"
        )

        # Display some example patients
        if filtered_results:
            self.stdout.write("\nTop 3 highest risk patients:")
            for r in sorted(
                filtered_results, key=lambda x: x["risk_score"], reverse=True
            )[:3]:
                self.stdout.write(
                    f"- Patient {r['patient_id'][:8]}: Risk score {r['risk_score']:.2f}, Days since contact: {r['days_since_contact']}"
                )

        # Generate output in requested format
        if output_format == "json" and filtered_results:
            output_file = f"inactive_patients_{datetime.now().strftime('%Y%m%d')}.json"
            with open(output_file, "w") as f:
                json.dump(filtered_results, f, indent=2)
            self.stdout.write(self.style.SUCCESS(f"Results saved to {output_file}"))

        elif output_format == "csv" and filtered_results:
            import csv

            output_file = f"inactive_patients_{datetime.now().strftime('%Y%m%d')}.csv"
            with open(output_file, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=filtered_results[0].keys())
                writer.writeheader()
                writer.writerows(filtered_results)
            self.stdout.write(self.style.SUCCESS(f"Results saved to {output_file}"))

        # Notify staff if requested and not skipped
        if notify and not skip_email and filtered_results:
            try:
                self._send_notification(filtered_results)
                self.stdout.write(self.style.SUCCESS("Notification sent to staff"))
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(
                        f"Could not send email notification: {str(e)}\n"
                        f"Check your email settings in settings.py or use --skip-email to bypass this error."
                    )
                )
                logger.warning(f"Email notification failed: {str(e)}")

        return filtered_results

    def _send_notification(self, results):
        """Send email notification to staff with list of inactive patients"""
        high_risk_count = sum(1 for r in results if r["risk_score"] > 0.8)

        subject = f"[Telepro-AI] {len(results)} patients need follow-up ({high_risk_count} high risk)"
        message = (
            f"The system has identified {len(results)} patients who need follow-up.\n\n"
            f"{high_risk_count} patients are at high risk (risk score > 0.8).\n\n"
            f"Please check the admin dashboard for details at: "
            f"{settings.SITE_URL}/admin/campaigns/campaign/inactive_patients/\n\n"
            f"This is an automated message from Telepro-AI."
        )

        admin_email = getattr(settings, "ADMIN_EMAIL", "admin@example.com")
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin_email],
            fail_silently=False,
        )
