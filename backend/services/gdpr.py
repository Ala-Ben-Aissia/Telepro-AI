import csv
import io
import json

from django.utils import timezone
from patients.models import Patient


class GDPRService:
    @staticmethod
    def export_patient_data(patient):
        """
        Export all patient data in a structured format
        """
        # Create a memory file-like object
        output = io.StringIO()

        # Write personal information
        writer = csv.writer(output)
        writer.writerow(["Data Export for Patient", str(patient.id)])
        writer.writerow(["Generated on", timezone.now().strftime("%Y-%m-%d %H:%M:%S")])
        writer.writerow([])

        # Personal information
        writer.writerow(["Personal Information"])
        writer.writerow(["Username", patient.user.username])
        writer.writerow(["Email", patient.email])
        writer.writerow(["Phone", patient.phone_number or "Not provided"])
        writer.writerow(["Date of Birth", patient.date_of_birth or "Not provided"])
        writer.writerow(["Gender", patient.gender or "Not provided"])
        writer.writerow(["Location", patient.location or "Not provided"])
        writer.writerow(["Language", patient.language_preference or "Not provided"])
        writer.writerow([])

        # Communication preferences
        writer.writerow(["Communication Preferences"])
        writer.writerow(["Contact Method", patient.preferred_contact_method])
        writer.writerow(["Email Verified", "Yes" if patient.email_verified else "No"])
        writer.writerow(["Phone Verified", "Yes" if patient.phone_verified else "No"])
        writer.writerow(["Has Consent", "Yes" if patient.has_active_consent else "No"])

        # Write contact time preferences as JSON
        writer.writerow(
            ["Contact Time Preferences", json.dumps(patient.contact_time_preferences)]
        )
        writer.writerow([])

        # Communication history
        writer.writerow(["Communication History"])
        writer.writerow(
            [
                "Last Contacted",
                patient.last_contacted_at.strftime("%Y-%m-%d %H:%M:%S")
                if patient.last_contacted_at
                else "Never",
            ]
        )
        writer.writerow(["Contact Attempts", patient.contact_attempts])
        writer.writerow(["Successful Contacts", patient.successful_contacts])
        writer.writerow([])

        # Get campaign history if available
        writer.writerow(["Campaign Communications"])
        writer.writerow(["Campaign", "Type", "Date", "Status"])

        from campaign.models import CommunicationLog

        comms = CommunicationLog.objects.filter(patient=patient).order_by("-sent_at")

        for comm in comms:
            writer.writerow(
                [
                    comm.campaign.title,
                    comm.communication_type,
                    comm.sent_at.strftime("%Y-%m-%d %H:%M:%S")
                    if comm.sent_at
                    else "Pending",
                    comm.status,
                ]
            )

        return output.getvalue()

    @staticmethod
    def process_deletion_requests():
        """
        Process scheduled deletion requests for patients
        """
        today = timezone.now().date()
        deletion_due = Patient.objects.filter(
            scheduled_deletion_date__lte=today, is_active=True
        )

        deleted_count = 0
        for patient in deletion_due:
            try:
                # Optional: Create deletion log
                # Log that we're deleting this patient

                # Anonymize first
                patient.anonymize()

                # Then deactivate
                patient.is_active = False
                patient.save()

                deleted_count += 1
            except Exception as e:
                # Log error
                pass

        return deleted_count
