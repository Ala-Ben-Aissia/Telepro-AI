import os
from datetime import datetime
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.db import transaction
from campaigns.models import Campaign, CampaignCategory, CommunicationLog, PatientSegment
from patients.models import Patient, ConsentRecord
from django.contrib.admin.models import LogEntry

User = get_user_model()


class Command(BaseCommand):
    help = "Backup all data to JSON and clear database except staff members"

    def add_arguments(self, parser):
        parser.add_argument(
            "--backup-dir",
            type=str,
            default="backups",
            help="Directory to store backup files",
        )
        parser.add_argument(
            "--format",
            type=str,
            default="json",
            choices=["json", "yaml", "xml"],
            help="Format for backup file",
        )
        parser.add_argument(
            "--confirm",
            action="store_true",
            help="Confirm data deletion without prompting",
        )

    def handle(self, *args, **options):
        backup_dir = options["backup_dir"]
        backup_format = options["format"]
        confirm = options["confirm"]

        # Create backup directory if it doesn't exist
        os.makedirs(backup_dir, exist_ok=True)

        # Generate timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"db_backup_{timestamp}.{backup_format}")

        # Step 1: Backup all data
        self.stdout.write(self.style.NOTICE(f"Backing up database to {backup_file}..."))
        try:
            call_command(
                "dumpdata",
                "--all",
                "--indent",
                "4",
                "--output",
                backup_file,
                "--format",
                backup_format,
                "--exclude",
                "contenttypes",
                "--exclude",
                "auth.permission",
            )
            self.stdout.write(
                self.style.SUCCESS(f"Database backed up successfully to {backup_file}")
            )

            # Create a summary of the backup
            self.create_backup_summary(backup_file, backup_format)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error backing up database: {str(e)}"))
            return

        # Step 2: Confirm before clearing data
        if not confirm:
            answer = input(
                "\nWARNING: This will delete all non-staff data from the database. Continue? (y/N): "
            )
            if answer.lower() != "y":
                self.stdout.write(self.style.WARNING("Operation cancelled."))
                return

        # Step 3: Clear database except staff members
        self.stdout.write(self.style.NOTICE("Clearing database except staff members..."))

        try:
            with transaction.atomic():
                # Get staff user IDs to preserve
                staff_user_ids = list(
                    User.objects.filter(is_staff=True).values_list("id", flat=True)
                )
                staff_count = len(staff_user_ids)

                # Get counts before deletion for reporting
                total_users = User.objects.count()
                total_patients = Patient.objects.count()
                total_campaigns = Campaign.objects.count()
                total_logs = CommunicationLog.objects.count()

                # Delete all non-staff users and related data
                CommunicationLog.objects.all().delete()
                # !!! important to delete communicationLogs at first to avoid the reference error since we're using protected foreign keys
                Patient.objects.all().delete()
                User.objects.filter(is_staff=False).delete()
                PatientSegment.objects.all().delete()
                Campaign.objects.all().delete()
                CampaignCategory.objects.all().delete()
                ConsentRecord.objects.all().delete()
                # Also delete all Django admin logs
                LogEntry.objects.all().delete()

                # Report what was deleted
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Database cleared successfully!\n"
                        f"Preserved: {staff_count} staff members\n"
                        f"Deleted: {total_users - staff_count} non-staff users\n"
                        f"Deleted: {total_patients} patients\n"
                        f"Deleted: {total_campaigns} campaigns\n"
                        f"Deleted: {total_logs} communication logs"
                    )
                )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error clearing database: {str(e)}"))

    def create_backup_summary(self, backup_file, backup_format):
        """Create a summary of what was backed up"""
        # Generate a summary file
        summary_file = backup_file.replace(f".{backup_format}", "_summary.txt")

        with open(summary_file, "w") as f:
            f.write(f"Backup Summary - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")

            # Count records of each model
            f.write("Record Counts:\n")
            f.write(f"Users: {User.objects.count()}\n")
            f.write(f"- Staff Users: {User.objects.filter(is_staff=True).count()}\n")
            f.write(f"- Patient Users: {User.objects.filter(is_staff=False).count()}\n")
            f.write(f"Patients: {Patient.objects.count()}\n")
            f.write(f"Campaigns: {Campaign.objects.count()}\n")
            f.write(f"Campaign Categories: {CampaignCategory.objects.count()}\n")
            f.write(f"Communication Logs: {CommunicationLog.objects.count()}\n")
            f.write(f"Consent Records: {ConsentRecord.objects.count()}\n")

        self.stdout.write(self.style.SUCCESS(f"Backup summary created at {summary_file}"))
