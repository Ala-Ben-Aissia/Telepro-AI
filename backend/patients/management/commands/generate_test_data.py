import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from django.contrib.auth import get_user_model

from patients.models import Patient, ConsentRecord
from campaigns.models import Campaign, CampaignCategory, CommunicationLog


User = get_user_model()


class Command(BaseCommand):
    help = "Generate test data for Telepro-AI"

    def add_arguments(self, parser):
        parser.add_argument(
            "--patients",
            type=int,
            default=100,
            help="Number of patient records to create",
        )
        parser.add_argument(
            "--staff", type=int, default=5, help="Number of staff users to create"
        )
        parser.add_argument(
            "--campaigns", type=int, default=10, help="Number of campaigns to create"
        )
        parser.add_argument(
            "--communications",
            type=int,
            default=500,
            help="Number of communication logs to create",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before generating new data",
        )

    def handle(self, *args, **options):
        num_patients = options["patients"]
        num_staff = options["staff"]
        num_campaigns = options["campaigns"]
        num_communications = options["communications"]
        clear_existing = options["clear"]

        # Display start message
        self.stdout.write(self.style.HTTP_INFO("Starting test data generation..."))
        if clear_existing:
            self.clear_data()

        # Generate the data in a transaction to ensure all or nothing
        with transaction.atomic():
            # Create staff users
            staff_users = self.create_staff_users(num_staff)
            self.stdout.write(f"Created {num_staff} staff users")

            # Create patient users and profiles
            patients = self.create_patient_users_and_profiles(num_patients, staff_users)
            self.stdout.write(f"Created {num_patients} patient users and profiles")

            # Create campaign categories
            categories = self.create_campaign_categories()
            self.stdout.write(f"Created {len(categories)} campaign categories")

            # Create campaigns
            campaigns = self.create_campaigns(num_campaigns, categories, staff_users)
            self.stdout.write(f"Created {num_campaigns} campaigns")

            # Create communication logs
            self.create_communication_logs(num_communications, campaigns, patients)
            self.stdout.write(f"Created {num_communications} communication logs")

            # Update engagement scores
            self.update_engagement_scores(patients)
            self.stdout.write("Updated patient engagement scores")

        self.stdout.write(self.style.SUCCESS("Test data generation completed!"))

    def clear_data(self):
        """Clear existing data from the database"""
        self.stdout.write("Clearing existing data...")

        # Only delete non-superuser users
        User.objects.filter(is_superuser=False).delete()

        # Other models will be deleted via cascade
        self.stdout.write(self.style.SUCCESS("Existing data cleared"))

    def create_staff_users(self, count):
        """Create staff users"""
        staff_users = []
        for i in range(count):
            username = f"staff{i + 1}"
            email = f"staff{i + 1}@example.com"

            user = User.objects.create_user(
                username=username,
                email=email,
                password="StaffPass123!",
                is_staff=True,
                user_type="STAFF",
                email_verified=True,
            )
            staff_users.append(user)
        return staff_users

    def create_patient_users_and_profiles(self, count, staff_users):
        """Create patient users and their profiles"""
        patients = []

        # Lists for realistic demographic distribution
        genders = ["M", "F", "O", "N"]
        gender_weights = [0.48, 0.48, 0.02, 0.02]  # Realistic distribution

        age_groups = ["0-18", "19-35", "36-50", "51-65", "65+"]
        age_weights = [0.15, 0.25, 0.25, 0.20, 0.15]  # Realistic distribution

        languages = ["fr", "en", "es", "ar", "de"]
        language_weights = [0.4, 0.3, 0.15, 0.1, 0.05]  # For a French-focused system

        locations = [
            "Paris",
            "Lyon",
            "Marseille",
            "Bordeaux",
            "Lille",
            "Toulouse",
            "Nantes",
            "Strasbourg",
            "Montpellier",
            "Nice",
            "Montreal",
            "Quebec",
            "Brussels",
            "Geneva",
            "Lausanne",
            "Algiers",
            "Tunis",
            "Rabat",
            "Casablanca",
            "Beirut",
        ]

        postal_codes = [
            "75001",
            "69001",
            "13001",
            "33000",
            "59000",
            "31000",
            "44000",
            "67000",
            "34000",
            "06000",
            "H2Y",
            "G1R",
            "1000",
            "1201",
            "1003",
            "16000",
            "1001",
            "10000",
            "20000",
            "1107",
        ]

        contact_methods = ["EMAIL", "SMS", "CALL", "NONE"]
        contact_method_weights = [0.6, 0.25, 0.05, 0.1]

        # Create patient users and profiles
        for i in range(count):
            # Create user
            username = f"patient{i + 1}"
            email = f"patient{i + 1}@example.com"
            phone = f"+33{600000000 + i}" if random.random() > 0.3 else None

            # Random demographics
            gender = random.choices(genders, weights=gender_weights)[0]
            age_group = random.choices(age_groups, weights=age_weights)[0]
            language = random.choices(languages, weights=language_weights)[0]
            location = random.choice(locations)
            postal_code = random.choice(postal_codes)
            contact_method = random.choices(
                contact_methods, weights=contact_method_weights
            )[0]

            # Randomize verification status
            email_verified = random.random() > 0.2
            phone_verified = random.random() > 0.4 if phone else False
            has_consent = random.random() > 0.15

            # Create user with encrypted data
            user = User.objects.create_user(
                username=username,
                email=email,
                password="PatientPass123!",
                is_staff=False,
                user_type="PATIENT",
                phone_number=phone,
                email_verified=email_verified,
                phone_verified=phone_verified,
            )

            # Get or create patient profile
            patient = Patient.objects.get(user=user)

            # Update patient fields
            patient.gender = gender
            patient.age_group = age_group
            patient.language_preference = language
            patient.location = location
            patient.postal_code = postal_code
            patient.preferred_contact_method = (
                contact_method if email_verified or phone_verified else "NONE"
            )
            patient.has_active_consent = has_consent

            # Random DOB based on age group
            year = 2023
            if age_group == "0-18":
                year = random.randint(2005, 2023)
            elif age_group == "19-35":
                year = random.randint(1988, 2004)
            elif age_group == "36-50":
                year = random.randint(1973, 1987)
            elif age_group == "51-65":
                year = random.randint(1958, 1972)
            else:  # 65+
                year = random.randint(1940, 1957)

            month = random.randint(1, 12)
            day = random.randint(1, 28)
            patient.date_of_birth = f"{year}-{month:02d}-{day:02d}"

            # Random engagement metrics
            patient.engagement_score = random.uniform(0, 1)

            # Random contact history
            patient.contact_attempts = random.randint(0, 20)
            patient.successful_contacts = random.randint(0, patient.contact_attempts)

            # Random activity dates
            days_ago = random.randint(0, 180)
            if days_ago > 0 and patient.contact_attempts > 0:
                patient.last_contacted_at = timezone.now() - timedelta(days=days_ago)

            response_days_ago = random.randint(0, 180)
            if response_days_ago > 0 and patient.successful_contacts > 0:
                patient.last_campaign_response = timezone.now() - timedelta(
                    days=response_days_ago
                )

            # Created by random staff user
            patient.created_by = random.choice(staff_users)

            # Save the patient
            patient.save()

            # Create consent records
            if has_consent:
                self.create_consent_records(patient, staff_users)

            patients.append(patient)

        return patients

    def create_consent_records(self, patient, staff_users):
        """Create consent records for a patient"""
        consent_types = [
            "GENERAL",
            "MARKETING",
            "RESEARCH",
            "THIRD_PARTY",
            "SENSITIVE_DATA",
            "AUTOMATED_DECISION",
        ]

        # Always create GENERAL consent (it's required for has_active_consent=True)
        ConsentRecord.objects.create(
            patient=patient,
            consent_type="GENERAL",
            granted=True,
            recorded_by=random.choice(staff_users) if random.random() > 0.5 else None,
            ip_address=f"192.168.1.{random.randint(2, 254)}",
            document_version="v1.0",
            consent_method=random.choice(["WEB_FORM", "API", "STAFF", "IMPORT"]),
        )

        # Create other consent types with weighted randomness
        for consent_type in consent_types[1:]:  # Skip GENERAL
            if random.random() > 0.3:  # 70% chance to have each additional consent
                ConsentRecord.objects.create(
                    patient=patient,
                    consent_type=consent_type,
                    granted=random.random() > 0.1,  # 90% chance to be granted
                    recorded_by=random.choice(staff_users)
                    if random.random() > 0.5
                    else None,
                    ip_address=f"192.168.1.{random.randint(2, 254)}",
                    document_version="v1.0",
                    consent_method=random.choice(["WEB_FORM", "API", "STAFF", "IMPORT"]),
                )

    def create_campaign_categories(self):
        """Create campaign categories"""
        categories = []

        category_data = [
            {
                "name": "Vaccination",
                "description": "Campagnes de vaccination",
                "is_active": True,
            },
            {
                "name": "Dépistage",
                "description": "Campagnes de dépistage de maladies",
                "is_active": True,
            },
            {
                "name": "Prévention",
                "description": "Campagnes de prévention",
                "is_active": True,
            },
            {
                "name": "Suivi médical",
                "description": "Suivi de patients avec conditions chroniques",
                "is_active": False,
            },
            {
                "name": "Santé mentale",
                "description": "Campagnes liées à la santé mentale",
                "is_active": True,
            },
            {
                "name": "Activité physique",
                "description": "Promotion de l'activité physique",
                "is_active": False,
            },
        ]

        for data in category_data:
            category, created = CampaignCategory.objects.get_or_create(
                name=data["name"],
                defaults={
                    "description": data["description"],
                    "is_active": data["is_active"],
                },
            )
            categories.append(category)

        return categories

    def create_campaigns(self, count, categories, staff_users):
        """Create test campaigns"""
        campaigns = []

        # Lists for campaign properties
        titles = [
            "Campagne de vaccination grippe",
            "Dépistage du cancer colorectal",
            "Prévention des maladies cardiovasculaires",
            "Suivi des patients diabétiques",
            "Sensibilisation à la santé mentale",
            "Promotion de l'activité physique",
            "Campagne contre le tabagisme",
            "Dépistage du cancer du sein",
            "Vaccination COVID-19",
            "Suivi des patients hypertendus",
            "Dépistage du diabète",
            "Santé bucco-dentaire",
            "Prévention des MST",
            "Suivi post-opératoire",
            "Campagne d'hydratation",
            "Vaccination HPV",
            "Santé des seniors",
            "Prévention des chutes chez les personnes âgées",
            "Campagne de don du sang",
            "Suivi nutritionnel",
        ]

        email_templates = [
            "<p>Bonjour {{username}},</p><p>Nous vous rappelons l'importance de {{campaign_title}}. Veuillez prendre rendez-vous en cliquant <a href='{{appointment_link}}'>ici</a>.</p>",
            "<p>Cher {{username}},</p><p>Avez-vous pensé à votre santé récemment? Notre {{campaign_title}} pourrait vous intéresser. <a href='{{appointment_link}}'>En savoir plus</a>.</p>",
            "<p>{{username}}, ne négligez pas votre santé!</p><p>Notre {{campaign_title}} est faite pour vous. <a href='{{appointment_link}}'>Prenez rendez-vous</a>.</p>",
        ]

        sms_templates = [
            "Bonjour {{username}}, rappel pour {{campaign_title}}. RDV: {{appointment_link}}",
            "{{username}}, participez à notre {{campaign_title}}. Infos: {{appointment_link}}",
            "Santé: {{campaign_title}} - Cliquez pour RDV {{appointment_link}}",
        ]

        # Generate campaigns
        for i in range(count):
            # If we've used all titles, start reusing with modifications
            if i < len(titles):
                title = titles[i]
            else:
                title = f"{random.choice(titles)} {i}"

            # Random dates
            end_days = random.randint(30, 365)
            start_days = random.randint(
                -30, end_days - 30
            )  # Some might have already started

            start_date = timezone.now() + timedelta(days=start_days)
            end_date = timezone.now() + timedelta(days=end_days)

            # Random target criteria
            target_age_groups = random.sample(
                ["0-18", "19-35", "36-50", "51-65", "65+"], k=random.randint(1, 5)
            )

            target_locations = random.sample(
                [
                    "Paris",
                    "Lyon",
                    "Marseille",
                    "Bordeaux",
                    "Montreal",
                    "Quebec",
                    "Tunis",
                    "Algiers",
                ],
                k=random.randint(1, 4),
            )

            target_languages = random.sample(["fr", "en", "ar"], k=random.randint(1, 3))

            # Create campaign
            campaign = Campaign.objects.create(
                title=title,
                category=random.choice(categories),
                description=f"Description pour {title}",
                start_date=start_date,
                end_date=end_date,
                is_active=random.random() > 0.2,  # 80% active
                target_age_groups=target_age_groups,
                target_locations=target_locations,
                target_languages=target_languages,
                email_template=random.choice(email_templates),
                sms_template=random.choice(sms_templates),
                created_by=random.choice(staff_users),
                updated_by=random.choice(staff_users),
            )

            campaigns.append(campaign)

        return campaigns

    def create_communication_logs(self, count, campaigns, patients):
        """Create communication logs"""
        statuses = ["PENDING", "SENT", "DELIVERED", "READ", "RESPONDED", "FAILED"]
        status_weights = [0.05, 0.1, 0.2, 0.3, 0.25, 0.1]  # Realistic distribution

        for i in range(count):
            # Select random campaign and patient
            campaign = random.choice(campaigns)
            patient = random.choice(patients)

            # Skip if patient doesn't have consent
            if not patient.has_active_consent:
                continue

            # Determine communication type based on patient preference
            if patient.preferred_contact_method == "NONE":
                comm_type = random.choice(["EMAIL", "SMS"])
            else:
                comm_type = patient.preferred_contact_method

            # Random status with weighted distribution
            status = random.choices(statuses, weights=status_weights)[0]

            # Calculate random dates
            sent_days_ago = random.randint(0, 90)
            sent_at = (
                timezone.now() - timedelta(days=sent_days_ago)
                if status != "PENDING"
                else None
            )

            delivered_at = None
            if status in ["DELIVERED", "READ", "RESPONDED"] and sent_at:
                delivered_at = sent_at + timedelta(minutes=random.randint(1, 120))

            read_at = None
            if status in ["READ", "RESPONDED"] and delivered_at:
                read_at = delivered_at + timedelta(minutes=random.randint(5, 600))

            # Random response for RESPONDED status
            response = ""
            if status == "RESPONDED" and read_at:
                responses = [
                    "Merci pour cette information, je vais prendre rendez-vous.",
                    "J'ai déjà pris rendez-vous, merci.",
                    "Pourriez-vous me donner plus d'informations?",
                    "Je ne suis pas intéressé pour le moment.",
                    "Merci, c'est noté.",
                ]
                response = random.choice(responses)

            # Random error for FAILED status
            error_message = ""
            if status == "FAILED":
                errors = [
                    "Email bounced: Invalid recipient",
                    "SMS delivery failed: Number unreachable",
                    "Network error",
                    "Rate limit exceeded",
                    "Invalid phone number format",
                ]
                error_message = random.choice(errors)

            # Create communication log
            comm_log = CommunicationLog.objects.create(
                campaign=campaign,
                patient=patient,
                communication_type=comm_type,
                status=status,
                sent_at=sent_at,
                delivered_at=delivered_at,
                read_at=read_at,
                response=response,
                error_message=error_message,
                metadata={
                    "attempt": random.randint(1, 3),
                    "send_hour": sent_at.hour if sent_at else random.randint(8, 18),
                },
            )

            # Update patient's last response time if applicable
            if status == "RESPONDED" and read_at:
                if (
                    not patient.last_campaign_response
                    or read_at > patient.last_campaign_response
                ):
                    patient.last_campaign_response = read_at
                    patient.save(update_fields=["last_campaign_response"])

    def update_engagement_scores(self, patients):
        """Update patient engagement scores based on communication logs"""
        for patient in patients:
            # Get communication logs for this patient
            logs = CommunicationLog.objects.filter(patient=patient)
            total = logs.count()

            if total > 0:
                # Calculate response rate
                responded = logs.filter(status="RESPONDED").count()
                read = logs.filter(status="READ").count()
                delivered = logs.filter(status="DELIVERED").count()

                # Calculate weighted engagement score (0-1)
                response_rate = responded / total
                read_rate = read / max(1, delivered)

                # More weight to responses
                engagement_score = (0.7 * response_rate) + (0.3 * read_rate)

                # Add some randomness for diversity
                engagement_score = min(
                    1.0, max(0.0, engagement_score + random.uniform(-0.1, 0.1))
                )

                # Update the patient
                patient.engagement_score = engagement_score
                patient.save(update_fields=["engagement_score"])
