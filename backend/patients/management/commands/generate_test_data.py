import random
import uuid
import math
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from django.contrib.auth import get_user_model
from patients.models import Patient, ConsentRecord
from campaigns.models import Campaign, CampaignCategory, CommunicationLog
import numpy as np  # Add numpy for better statistical distribution generation

User = get_user_model()


class Command(BaseCommand):
    help = "Generate test data for Telepro-AI machine learning training"

    def add_arguments(self, parser):
        parser.add_argument(
            "--patients",
            type=int,
            default=200,  # Increased for better statistical significance
            help="Number of patient records to create",
        )
        parser.add_argument(
            "--staff", type=int, default=5, help="Number of staff users to create"
        )
        parser.add_argument(
            "--campaigns", type=int, default=15, help="Number of campaigns to create"
        )
        parser.add_argument(
            "--communications",
            type=int,
            default=2000,  # Increased for better ML training
            help="Number of communication logs to create",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before generating new data",
        )
        # New parameter to control the correlation strength
        parser.add_argument(
            "--correlation",
            type=float,
            default=0.7,  # 1.0 for perfect correlation, 0.0 for no correlation (random)
            help="Correlation strength between patient attributes and outcomes (0-1)",
        )

    def handle(self, *args, **options):
        num_patients = options["patients"]
        num_staff = options["staff"]
        num_campaigns = options["campaigns"]
        num_communications = options["communications"]
        clear_existing = options["clear"]
        self.correlation_strength = options["correlation"]

        # Store cohorts for more realistic patterns
        self.patient_cohorts = {}
        self.campaign_effectiveness = {}

        # Display start message
        self.stdout.write(
            self.style.HTTP_INFO("Starting ML-optimized test data generation...")
        )
        if clear_existing:
            self.clear_data()

        # Generate the data in a transaction to ensure all or nothing
        with transaction.atomic():
            # Create staff users
            staff_users = self.create_staff_users(num_staff)
            self.stdout.write(f"Created {num_staff} staff users")

            # Create campaign categories with predefined effectiveness
            categories = self.create_campaign_categories()
            self.stdout.write(
                f"Created {len(categories)} campaign categories with predefined effectiveness rates"
            )

            # Create campaigns with weighted effectiveness based on category
            campaigns = self.create_campaigns(num_campaigns, categories, staff_users)
            self.stdout.write(
                f"Created {num_campaigns} campaigns with realistic effectiveness profiles"
            )

            # Create patient cohorts with distinct characteristics
            self.generate_patient_cohorts()
            self.stdout.write(
                "Generated patient cohorts with distinct behavioral patterns"
            )

            # Create patient users and profiles with cohort-based characteristics
            patients = self.create_patient_users_and_profiles(num_patients, staff_users)
            self.stdout.write(
                f"Created {num_patients} patient users with cohort-based profiles"
            )
            # The validation summary will be printed after patient creation (see validation code in create_patient_users_and_profiles)

            # --- Generate Patient Segments ---
            from campaigns.models import PatientSegment
            segments = [
                {
                    "name": "Young Urban Adults",
                    "description": "Patients aged 19-35 living in major cities.",
                    "criteria": {"age_group": ["19-35"], "location": ["Paris", "Montreal", "Toulouse"]}
                },
                {
                    "name": "Seniors",
                    "description": "Patients aged 65+.",
                    "criteria": {"age_group": ["65+"]}
                },
                {
                    "name": "Engaged Patients",
                    "description": "Patients with engagement_score > 0.5.",
                    "criteria": {"engagement_score__gt": 0.5}
                },
                {
                    "name": "Consent-Active",
                    "description": "Patients with active consent for marketing.",
                    "criteria": {"has_active_consent": True}
                },
            ]
            for seg in segments:
                PatientSegment.objects.create(**seg)
            self.stdout.write(self.style.SUCCESS(f"Created {len(segments)} patient segments with realistic criteria."))

            # Create communication logs with realistic response patterns
            self.create_communication_logs(num_communications, campaigns, patients)
            self.stdout.write(
                f"Created {num_communications} communication logs with realistic response patterns"
            )

            # Update engagement scores based on cohort and communication history
            self.update_engagement_scores(patients)
            self.stdout.write(
                "Updated patient engagement scores with realistic distributions"
            )

            # Create temporal patterns in the data
            self.create_temporal_patterns(patients, campaigns)
            self.stdout.write("Added temporal patterns to the data")

        self.stdout.write(
            self.style.SUCCESS("ML-optimized test data generation completed!")
        )

    def generate_patient_cohorts(self):
        """Generate patient cohorts with distinct behavioral characteristics"""
        # Define cohorts with distinct characteristics
        self.cohorts = {
            "highly_engaged": {
                "weight": 0.15,  # 15% of patients
                "base_response_rate": 0.8,
                "base_engagement": 0.85,
                "preferred_methods": {"EMAIL": 0.7, "SMS": 0.25, "CALL": 0.05},
                "consent_likelihood": 0.95,
                "age_distribution": {
                    "0-18": 0.05,
                    "19-35": 0.3,
                    "36-50": 0.4,
                    "51-65": 0.2,
                    "65+": 0.05,
                },
            },
            "moderate_engaged": {
                "weight": 0.40,  # 40% of patients
                "base_response_rate": 0.5,
                "base_engagement": 0.6,
                "preferred_methods": {
                    "EMAIL": 0.6,
                    "SMS": 0.3,
                    "CALL": 0.05,
                    "NONE": 0.05,
                },
                "consent_likelihood": 0.85,
                "age_distribution": {
                    "0-18": 0.1,
                    "19-35": 0.25,
                    "36-50": 0.3,
                    "51-65": 0.25,
                    "65+": 0.1,
                },
            },
            "low_engaged": {
                "weight": 0.30,  # 30% of patients
                "base_response_rate": 0.2,
                "base_engagement": 0.3,
                "preferred_methods": {"EMAIL": 0.4, "SMS": 0.3, "CALL": 0.1, "NONE": 0.2},
                "consent_likelihood": 0.6,
                "age_distribution": {
                    "0-18": 0.15,
                    "19-35": 0.2,
                    "36-50": 0.2,
                    "51-65": 0.2,
                    "65+": 0.25,
                },
            },
            "non_responsive": {
                "weight": 0.15,  # 15% of patients
                "base_response_rate": 0.05,
                "base_engagement": 0.1,
                "preferred_methods": {"EMAIL": 0.3, "SMS": 0.2, "CALL": 0.1, "NONE": 0.4},
                "consent_likelihood": 0.3,
                "age_distribution": {
                    "0-18": 0.2,
                    "19-35": 0.15,
                    "36-50": 0.15,
                    "51-65": 0.2,
                    "65+": 0.3,
                },
            },
        }

        # Create category effectiveness profiles
        self.category_effectiveness = {
            "Vaccination": {
                "base_effectiveness": 0.65,
                "age_factors": {
                    "0-18": 0.9,
                    "19-35": 0.6,
                    "36-50": 0.7,
                    "51-65": 0.8,
                    "65+": 0.9,
                },
                "seasonal_effect": True,
            },
            "Dépistage": {
                "base_effectiveness": 0.55,
                "age_factors": {
                    "0-18": 0.3,
                    "19-35": 0.5,
                    "36-50": 0.8,
                    "51-65": 0.9,
                    "65+": 0.8,
                },
                "seasonal_effect": False,
            },
            "Prévention": {
                "base_effectiveness": 0.6,
                "age_factors": {
                    "0-18": 0.7,
                    "19-35": 0.6,
                    "36-50": 0.7,
                    "51-65": 0.7,
                    "65+": 0.6,
                },
                "seasonal_effect": False,
            },
            "Suivi médical": {
                "base_effectiveness": 0.7,
                "age_factors": {
                    "0-18": 0.5,
                    "19-35": 0.4,
                    "36-50": 0.6,
                    "51-65": 0.8,
                    "65+": 0.9,
                },
                "seasonal_effect": False,
            },
            "Santé mentale": {
                "base_effectiveness": 0.5,
                "age_factors": {
                    "0-18": 0.7,
                    "19-35": 0.8,
                    "36-50": 0.6,
                    "51-65": 0.5,
                    "65+": 0.4,
                },
                "seasonal_effect": True,
            },
            "Activité physique": {
                "base_effectiveness": 0.45,
                "age_factors": {
                    "0-18": 0.8,
                    "19-35": 0.7,
                    "36-50": 0.6,
                    "51-65": 0.4,
                    "65+": 0.2,
                },
                "seasonal_effect": True,
            },
        }
        # Updated location weights based on metropolitan area populations
        self.location_weights = {
            # Major French cities
            "Paris": 0.24,  # ~12.5M metro area
            "Lyon": 0.05,  # ~2.3M metro area
            "Marseille": 0.04,  # ~1.7M metro area
            "Lille": 0.03,  # ~1.2M metro area
            "Toulouse": 0.03,  # ~1.3M metro area
            "Bordeaux": 0.03,  # ~1.2M metro area
            "Nice": 0.02,  # ~1.0M metro area
            "Nantes": 0.02,  # ~950K metro area
            "Strasbourg": 0.02,  # ~780K metro area
            "Montpellier": 0.01,  # ~600K metro area
            # Major French-speaking cities outside France
            "Montreal": 0.08,  # ~4.2M metro area
            "Brussels": 0.04,  # ~2.1M metro area
            "Quebec": 0.02,  # ~800K metro area
            "Geneva": 0.01,  # ~600K metro area
            "Lausanne": 0.01,  # ~420K metro area
            # North African cities with Francophone populations
            "Algiers": 0.15,  # ~7.8M metro area
            "Casablanca": 0.13,  # ~6.8M metro area
            "Tunis": 0.05,  # ~2.7M metro area
            "Rabat": 0.04,  # ~1.8M metro area
            "Beirut": 0.04,  # ~2.2M metro area
        }

    def create_patient_users_and_profiles(self, count, staff_users):
        """Create patient users and their profiles with cohort-based characteristics"""
        patients = []

        # Lists for demographic distribution
        genders = ["M", "F", "O", "N"]
        gender_weights = [0.48, 0.48, 0.02, 0.02]  # Realistic distribution

        languages = ["fr", "en", "es", "ar", "de"]
        language_weights = [0.4, 0.3, 0.15, 0.1, 0.05]  # For a French-focused system

        # Locations based on metropolitan area populations
        locations = list(self.location_weights.keys())
        location_dist = list(self.location_weights.values())

        # Postal codes linked to locations
        postal_code_map = {
            "Paris": ["75001", "75002", "75003", "75004", "75005"],
            "Lyon": ["69001", "69002", "69003"],
            "Marseille": ["13001", "13002", "13003"],
            # Add mappings for all other locations
        }

        # Assign cohorts to patients with predefined weights
        cohort_names = list(self.cohorts.keys())
        cohort_weights = [self.cohorts[c]["weight"] for c in cohort_names]

        # Create patient users and profiles
        for i in range(count):
            # Assign a cohort based on weights
            cohort = np.random.choice(cohort_names, p=cohort_weights)
            cohort_data = self.cohorts[cohort]

            # Store cohort for later use
            patient_id = str(uuid.uuid4())
            self.patient_cohorts[patient_id] = cohort

            # Create user with cohort-influenced data
            username = f"patient{i + 1}"
            email = f"patient{i + 1}@example.com"

            # Phone number based on cohort (higher engagement = more likely to have phone)
            has_phone = random.random() < (0.3 + cohort_data["base_engagement"] / 2)
            phone = f"+33{600000000 + i}" if has_phone else None

            # Demographics influenced by cohort
            gender = random.choices(genders, weights=gender_weights)[0]

            # Age group from cohort-specific distribution
            age_distribution = cohort_data["age_distribution"]
            age_groups = list(age_distribution.keys())
            age_weights = list(age_distribution.values())
            age_group = random.choices(age_groups, weights=age_weights)[0]

            language = random.choices(languages, weights=language_weights)[0]
            location = random.choices(locations, weights=location_dist)[0]

            # Postal code based on location
            if location in postal_code_map:
                postal_code = random.choice(postal_code_map[location])
            else:
                postal_code = random.choice(
                    [
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
                    ]
                )

            # Contact method from cohort-specific distribution
            preferred_methods = cohort_data["preferred_methods"]
            methods = list(preferred_methods.keys())
            method_weights = list(preferred_methods.values())
            contact_method = random.choices(methods, weights=method_weights)[0]

            # Verification status influenced by engagement level
            email_verified = random.random() < (0.6 + cohort_data["base_engagement"] / 3)
            phone_verified = (
                random.random() < (0.4 + cohort_data["base_engagement"] / 3)
                if phone
                else False
            )

            # Consent based on cohort
            has_consent = random.random() < cohort_data["consent_likelihood"]

            # Create user
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

            # Get patient profile
            patient = Patient.objects.get(user=user)
            # patient.id = patient_id  # Set the UUID we generated earlier
            # handled behind the scenes through signals.

            # Update patient fields
            patient.gender = gender
            patient.age_group = age_group
            patient.language_preference = language
            patient.location = location
            patient.postal_code = postal_code
            patient.preferred_contact_method = (
                contact_method if (email_verified or phone_verified) else "NONE"
            )
            patient.has_active_consent = has_consent

            # Date of birth aligned with age group
            current_year = timezone.now().year
            if age_group == "0-18":
                year = random.randint(current_year - 18, current_year)
            elif age_group == "19-35":
                year = random.randint(current_year - 35, current_year - 19)
            elif age_group == "36-50":
                year = random.randint(current_year - 50, current_year - 36)
            elif age_group == "51-65":
                year = random.randint(current_year - 65, current_year - 51)
            else:  # 65+
                year = random.randint(current_year - 90, current_year - 66)

            month = random.randint(1, 12)
            day = random.randint(1, 28)
            patient.date_of_birth = f"{year}-{month:02d}-{day:02d}"

            # Engagement metrics aligned with cohort
            base_engagement = cohort_data["base_engagement"]
            # Add some noise to engagement
            variance = 0.15  # How much engagement can vary from the cohort baseline
            patient.engagement_score = max(
                0, min(1, base_engagement + random.uniform(-variance, variance))
            )

            # Record dates influenced by engagement
            contact_days = int(
                365 * (1 - patient.engagement_score)
            )  # Less engaged = longer time since contact
            contact_days = max(
                0, min(365, contact_days + random.randint(-30, 30))
            )  # Add some noise

            if contact_days > 0:
                patient.last_contacted_at = timezone.now() - timedelta(days=contact_days)

            response_days = int(
                contact_days * 1.2
            )  # Response usually older than last contact
            response_days = max(0, min(365, response_days))

            if response_days > 0 and has_consent:
                patient.last_campaign_response = timezone.now() - timedelta(
                    days=response_days
                )

            # Created by random staff user
            patient.created_by = random.choice(staff_users)

            # Save the patient
            patient.save()

            # Create consent records if appropriate
            if has_consent:
                self.create_realistic_consent_records(patient, staff_users, cohort_data)

            patients.append(patient)

        # --- Automated Validation of Generated Patient Data ---
        valid_patients = []
        invalid_patients = []
        for patient in patients:
            errors = []
            if not patient.gender or patient.gender not in ["M", "F", "O", "N"]:
                errors.append("Invalid or missing gender")
            if not patient.age_group or patient.age_group not in ["0-18", "19-35", "36-50", "51-65", "65+"]:
                errors.append("Invalid or missing age_group")
            if not patient.location:
                errors.append("Missing location")
            if not patient.language_preference or patient.language_preference not in ["fr", "en", "es", "ar", "de"]:
                errors.append("Invalid or missing language_preference")
            if patient.engagement_score is None or not (0 <= patient.engagement_score <= 1):
                errors.append("Invalid or missing engagement_score")
            if patient.has_active_consent not in [True, False]:
                errors.append("Missing has_active_consent")
            if not patient.preferred_contact_method:
                errors.append("Missing preferred_contact_method")
            if errors:
                invalid_patients.append((patient, errors))
            else:
                valid_patients.append(patient)
        if invalid_patients:
            from django.core.management.base import CommandError
            self.stdout.write(self.style.WARNING(f"Validation: {len(invalid_patients)} invalid patient records found."))
            for patient, errs in invalid_patients[:5]:
                self.stdout.write(self.style.WARNING(f"  - Patient ID {patient.id}: {', '.join(errs)}"))
            if len(invalid_patients) > 5:
                self.stdout.write(self.style.WARNING(f"  ...and {len(invalid_patients)-5} more."))
        self.stdout.write(self.style.SUCCESS(f"Validation: {len(valid_patients)} valid patient records generated."))
        return valid_patients

    def create_realistic_consent_records(self, patient, staff_users, cohort_data):
        """Create consent records with patterns based on patient cohort"""
        consent_types = [
            "GENERAL",
            "MARKETING",
            "RESEARCH",
            "THIRD_PARTY",
            "SENSITIVE_DATA",
            "AUTOMATED_DECISION",
        ]

        # More engaged patients are more likely to consent to more types
        base_consent = cohort_data["consent_likelihood"]

        # Always create GENERAL consent for patients with has_active_consent=True
        ConsentRecord.objects.create(
            patient=patient,
            consent_type="GENERAL",
            granted=True,
            recorded_by=random.choice(staff_users) if random.random() > 0.5 else None,
            ip_address=f"192.168.1.{random.randint(2, 254)}",
            document_version="v1.0",
            consent_method=random.choice(["WEB_FORM", "API", "STAFF", "IMPORT"]),
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        )

        # Create other consent types with weights that diminish for less sensitive types
        for i, consent_type in enumerate(consent_types[1:]):
            # More sensitive consent types get progressively lower likelihood
            consent_factor = 1.0 - (i * 0.15)
            if random.random() < base_consent * consent_factor:
                # Highly engaged patients almost always grant consent
                granted = random.random() < (0.8 + cohort_data["base_engagement"] / 5)

                ConsentRecord.objects.create(
                    patient=patient,
                    consent_type=consent_type,
                    granted=granted,
                    recorded_by=random.choice(staff_users)
                    if random.random() > 0.5
                    else None,
                    ip_address=f"192.168.1.{random.randint(2, 254)}",
                    document_version="v1.0",
                    consent_method=random.choice(["WEB_FORM", "API", "STAFF", "IMPORT"]),
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                )

    def create_communication_logs(self, count, campaigns, patients):
        """Create communication logs with realistic response patterns"""
        # Status transition probabilities (markov chain)
        status_transitions = {
            "SENT": {"DELIVERED": 0.85, "FAILED": 0.15},
            "DELIVERED": {
                "READ": 0.65,
                "DELIVERED": 0.35,
            },  # Some delivered but never read
            "READ": {"RESPONDED": 0.4, "READ": 0.6},  # Some read but never respond
        }

        completed_logs = 0
        attempts = 0
        max_attempts = count * 2  # Allow up to 2x attempts to reach desired count

        while completed_logs < count and attempts < max_attempts:
            attempts += 1

            # Select random campaign and patient with weightings
            campaign = random.choice(campaigns)
            patient = random.choice(patients)

            # Skip if patient doesn't have consent
            if not patient.has_active_consent:
                continue

            # Check if patient is in a target group for this campaign
            matches_age_group = patient.age_group in campaign.target_age_groups
            matches_location = patient.location in campaign.target_locations
            matches_language = patient.language_preference in campaign.target_languages

            # Calculate match score (0-1)
            match_score = (
                (0.4 if matches_age_group else 0)
                + (0.3 if matches_location else 0)
                + (0.3 if matches_language else 0)
            )

            # Only proceed for reasonable matches or by random chance
            if match_score < 0.4 and random.random() > 0.2:
                continue

            # Get patient cohort info
            cohort = self.patient_cohorts.get(str(patient.id), "moderate_engaged")
            cohort_data = self.cohorts[cohort]

            # Determine communication type based on patient preference
            if patient.preferred_contact_method == "NONE":
                comm_type = random.choice(["EMAIL", "SMS"])
            else:
                comm_type = patient.preferred_contact_method

            # Influence outcome based on patient cohort and campaign match
            base_response_rate = cohort_data["base_response_rate"]
            # Modify by match score - well-matched campaigns get better response
            modified_response_rate = base_response_rate * (0.5 + 0.5 * match_score)

            # Determine starting status - all start as SENT
            status = "SENT"

            # Simulate the communication flow through different statuses
            sent_at = None
            delivered_at = None
            read_at = None

            # Calculate random dates - more recent for engaged patients
            engagement_factor = patient.engagement_score
            max_days_ago = 90 * (1 - engagement_factor / 2)  # More engaged = more recent
            sent_days_ago = random.randint(0, int(max_days_ago))
            sent_at = timezone.now() - timedelta(days=sent_days_ago)

            # Decide final status through markov transitions
            while status in ["SENT", "DELIVERED", "READ"]:
                if status in status_transitions:
                    next_statuses = list(status_transitions[status].keys())
                    next_probs = list(status_transitions[status].values())

                    # Adjust transition probabilities based on patient engagement and campaign match
                    if status == "READ" and "RESPONDED" in next_statuses:
                        idx = next_statuses.index("RESPONDED")
                        # Increase response probability for engaged patients and good matches
                        response_boost = (
                            modified_response_rate * self.correlation_strength
                        )
                        adjusted_probs = next_probs.copy()
                        adjusted_probs[idx] = min(0.95, next_probs[idx] + response_boost)
                        # Normalize probabilities
                        total = sum(adjusted_probs)
                        next_probs = [p / total for p in adjusted_probs]

                    next_status = random.choices(next_statuses, weights=next_probs)[0]

                    # If status didn't change, we're done
                    if next_status == status:
                        break

                    status = next_status

                    # Set appropriate timestamps
                    if status == "DELIVERED":
                        # Delivered within minutes to hours
                        delivered_delay = random.randint(1, 120)  # 1-120 minutes
                        delivered_at = sent_at + timedelta(minutes=delivered_delay)
                    elif status == "READ":
                        # Read within hours to days
                        read_delay = random.randint(10, 60 * 48)  # 10 min to 48 hours
                        read_at = delivered_at + timedelta(minutes=read_delay)
                    # RESPONDED status handled below
                else:
                    break

            # If we ended with FAILED, set appropriate error
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

            # For RESPONDED status, generate realistic response text
            response = ""
            if status == "RESPONDED":
                # More positive responses for engaged patients and good matches
                positivity = patient.engagement_score * match_score

                if positivity > 0.7:
                    responses = [
                        "Merci pour cette information, je vais prendre rendez-vous immédiatement.",
                        "C'est exactement ce dont j'avais besoin, j'ai déjà pris rendez-vous.",
                        "Parfait, j'apprécie beaucoup cette information utile.",
                    ]
                elif positivity > 0.4:
                    responses = [
                        "Merci pour cette information, je vais y réfléchir.",
                        "J'ai déjà pris rendez-vous, merci du rappel.",
                        "Je vais consulter mon emploi du temps et revenir vers vous.",
                    ]
                else:
                    responses = [
                        "Je ne suis pas intéressé pour le moment.",
                        "Merci, mais je n'ai pas besoin de ce service actuellement.",
                        "Veuillez me retirer de votre liste de diffusion.",
                    ]

                response = random.choice(responses)

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
                    "send_hour": sent_at.hour if sent_at else random.randint(8, 18),
                    "send_day": sent_at.strftime("%A")
                    if sent_at
                    else random.choice(
                        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
                    ),
                    "match_score": match_score,
                    "device": random.choice(["mobile", "desktop", "tablet"])
                    if status in ["READ", "RESPONDED"]
                    else None,
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

            # Only count completed logs
            completed_logs += 1

    def create_temporal_patterns(self, patients, campaigns):
        """Add seasonal and temporal patterns to make data more realistic"""
        # Get all communication logs
        all_logs = CommunicationLog.objects.all()

        # Simulate seasonal effects
        months = range(1, 13)
        # Response rates by month (higher in fall/winter for vaccines, etc.)
        monthly_factors = {
            1: 1.2,  # January
            2: 1.1,  # February
            3: 1.0,  # March
            4: 0.9,  # April
            5: 0.8,  # May
            6: 0.7,  # June
            7: 0.6,  # July
            8: 0.7,  # August
            9: 0.9,  # September
            10: 1.1,  # October
            11: 1.2,  # November
            12: 1.1,  # December
        }

        # Apply monthly patterns to a subset of logs
        for log in all_logs:
            if log.sent_at and random.random() < 0.8:  # Apply to 80% of logs
                # Get month and its factor
                month = log.sent_at.month
                factor = monthly_factors[month]

                # Campaigns with seasonal effect have stronger monthly patterns
                if (
                    log.campaign.category
                    and log.campaign.category.name in self.category_effectiveness
                ):
                    category_data = self.category_effectiveness[
                        log.campaign.category.name
                    ]
                    if category_data.get("seasonal_effect", False):
                        factor = factor**1.5  # Amplify seasonal effect

                # Determine if status should change based on month
                if log.status == "READ" and random.random() < 0.3 * factor:
                    # Winter months more likely to convert READ to RESPONDED
                    log.status = "RESPONDED"
                    log.response = "Suite à votre campagne saisonnière, j'ai décidé de prendre rendez-vous."
                    log.save(update_fields=["status", "response"])

        # Add time-of-day patterns
        # Morning (8-11): Good for older demographics
        # Afternoon (12-17): Good for working adults
        # Evening (18-22): Good for younger demographics

        time_patterns = {
            "0-18": {"peak_hours": [16, 17, 18, 19, 20, 21], "factor": 1.3},
            "19-35": {"peak_hours": [12, 13, 18, 19, 20, 21, 22], "factor": 1.25},
            "36-50": {"peak_hours": [7, 8, 12, 13, 19, 20], "factor": 1.2},
            "51-65": {"peak_hours": [9, 10, 11, 14, 15, 16], "factor": 1.15},
            "65+": {"peak_hours": [9, 10, 11, 14, 15], "factor": 1.3},
        }

        # Apply time patterns to a subset of logs with RESPONDED status
        responded_logs = CommunicationLog.objects.filter(status="RESPONDED")
        for log in responded_logs:
            if log.sent_at and random.random() < 0.7:  # Apply to 70% of logs
                # Get patient age group
                age_group = log.patient.age_group
                if age_group in time_patterns:
                    pattern = time_patterns[age_group]
                    hour = log.sent_at.hour
                    # If sent during peak hours for this age group, potentially make it more effective
                    if hour in pattern["peak_hours"]:
                        # For logs that are READ but not yet RESPONDED, maybe upgrade to RESPONDED
                        if (
                            log.status == "READ"
                            and random.random() < 0.4 * pattern["factor"]
                        ):
                            log.status = "RESPONDED"
                            log.response = "Cette heure de la journée me convenait parfaitement pour répondre."
                            log.save(update_fields=["status", "response"])

        self.stdout.write("Added time-of-day patterns based on demographic preferences")

        # Add day-of-week patterns
        weekday_response_factors = {
            0: 1.1,  # Monday
            1: 1.2,  # Tuesday
            2: 1.3,  # Wednesday
            3: 1.2,  # Thursday
            4: 0.9,  # Friday
            5: 0.8,  # Saturday
            6: 0.7,  # Sunday
        }

        for log in all_logs:
            if log.sent_at and random.random() < 0.6:  # Apply to 60% of logs
                weekday = log.sent_at.weekday()
                factor = weekday_response_factors[weekday]

                # Modify metadata to reflect day influence
                metadata = log.metadata or {}
                metadata["weekday_factor"] = factor
                log.metadata = metadata
                log.save(update_fields=["metadata"])

    def update_engagement_scores(self, patients):
        """
        Update patient engagement scores with a more sophisticated algorithm
        that takes into account recency, frequency, and cumulative interactions
        """
        for patient in patients:
            # Get communication logs for this patient
            logs = CommunicationLog.objects.filter(patient=patient)
            total = logs.count()

            if total > 0:
                # Basic metrics
                responded = logs.filter(status="RESPONDED").count()
                read = logs.filter(status="READ").count()
                delivered = logs.filter(status="DELIVERED").count()
                failed = logs.filter(status="FAILED").count()

                # Response rate with higher weight
                if total > 0:
                    response_rate = responded / total
                    read_rate = read / max(1, delivered + read + responded)
                else:
                    response_rate = 0
                    read_rate = 0

                # Recency factor - more recent interactions get more weight
                now = timezone.now()
                recency_factor = 0.5

                if patient.last_campaign_response:
                    days_since_response = (now - patient.last_campaign_response).days
                    # Exponential decay: recent responses matter more
                    recency_factor += 0.5 * math.exp(-days_since_response / 60)

                # Calculate cohort-influenced engagement score
                cohort = self.patient_cohorts.get(str(patient.id), "moderate_engaged")
                base_engagement = self.cohorts[cohort]["base_engagement"]

                # Combine factors with weights
                engagement_score = (
                    0.4 * response_rate  # Response rate most important
                    + 0.2 * read_rate  # Read rate somewhat important
                    + 0.2 * recency_factor  # Recency factor for timeliness
                    + 0.2 * base_engagement  # Base cohort tendency
                )

                # Add small random noise
                engagement_score = min(
                    1.0, max(0.0, engagement_score + random.uniform(-0.05, 0.05))
                )

                # Update the patient
                patient.engagement_score = engagement_score
                patient.save(update_fields=["engagement_score"])

    def clear_data(self):
        """Clear existing data from the database, handling protected relationships."""
        self.stdout.write("Clearing existing data...")

        # Delete related objects first to avoid ProtectedError
        from campaigns.models import Campaign, CampaignCategory, CommunicationLog, PatientSegment
        from patients.models import Patient, ConsentRecord

        CommunicationLog.objects.all().delete()
        PatientSegment.objects.all().delete()
        Campaign.objects.all().delete()
        CampaignCategory.objects.all().delete()
        ConsentRecord.objects.all().delete()
        Patient.objects.all().delete()

        # Only delete non-superuser users (after related objects are gone)
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write(self.style.SUCCESS("Existing data cleared"))

    def create_staff_users(self, count):
        """Create staff users"""
        staff_users = []
        previous_staff = User.objects.filter(is_staff=True)
        for i in range(count):
            username = f"staff{i + previous_staff.count() + 1}"
            email = f"staff{i + previous_staff.count() + 1}@example.com"

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

    def create_campaign_categories(self):
        """Create campaign categories with realistic effectiveness patterns"""
        categories = []

        category_data = [
            {
                "name": "Vaccination",
                "description": "Campagnes de vaccination avec efficacité saisonnière",
                "is_active": True,
                "base_effectiveness": 0.65,
            },
            {
                "name": "Dépistage",
                "description": "Campagnes de dépistage ciblant des populations spécifiques",
                "is_active": True,
                "base_effectiveness": 0.55,
            },
            {
                "name": "Prévention",
                "description": "Campagnes de prévention générale",
                "is_active": True,
                "base_effectiveness": 0.60,
            },
            {
                "name": "Suivi médical",
                "description": "Suivi de patients avec conditions chroniques",
                "is_active": False,
                "base_effectiveness": 0.70,
            },
            {
                "name": "Santé mentale",
                "description": "Campagnes liées à la santé mentale avec variabilité saisonnière",
                "is_active": True,
                "base_effectiveness": 0.50,
            },
            {
                "name": "Activité physique",
                "description": "Promotion de l'activité physique avec forte saisonnalité",
                "is_active": False,
                "base_effectiveness": 0.45,
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
            # Store effectiveness data for later use
            self.campaign_effectiveness[data["name"]] = data["base_effectiveness"]
            categories.append(category)

        return categories

    def create_campaigns(self, count, categories, staff_users):
        """Create campaigns with realistic effectiveness patterns and content"""
        campaigns = []

        # More realistic and diverse campaign titles
        titles = [
            "Campagne de vaccination grippe saisonnière",
            "Dépistage précoce du cancer colorectal",
            "Prévention des maladies cardiovasculaires",
            "Suivi régulier pour patients diabétiques",
            "Sensibilisation à la santé mentale en milieu professionnel",
            "Programme d'activité physique pour seniors",
            "Campagne contre le tabagisme chez les jeunes",
            "Dépistage du cancer du sein - Octobre Rose",
            "Vaccination COVID-19 - Rappel annuel",
            "Suivi personnalisé des patients hypertendus",
            "Dépistage du diabète de type 2",
            "Santé bucco-dentaire - Contrôle annuel",
            "Prévention des MST chez les 18-25 ans",
            "Suivi post-opératoire personnalisé",
            "Campagne d'hydratation pour l'été",
            "Vaccination HPV pour adolescents",
            "Santé des seniors - Prévention des chutes",
            "Programme de nutrition équilibrée",
            "Campagne de don du sang",
            "Bien-être mental en période hivernale",
            "Programme de réduction du stress",
            "Campagne de sensibilisation aux allergies saisonnières",
            "Suivi des maladies chroniques respiratoires",
            "Prévention des risques liés à la canicule",
        ]

        # Create richer templates with more personalization options
        email_templates = [
            "<p>Bonjour {{username}},</p><p>Nous vous rappelons l'importance de {{campaign_title}}. Votre santé est notre priorité, et votre prochain rendez-vous devrait être planifié prochainement.</p><p>Veuillez prendre rendez-vous en cliquant <a href='{{appointment_link}}'>ici</a>.</p><p>Cordialement,<br>L'équipe médicale</p>",
            "<p>Cher(e) {{username}},</p><p>Avez-vous pensé à votre santé récemment? Notre {{campaign_title}} pourrait vous intéresser particulièrement en raison de votre profil de santé.</p><p>Nous offrons des créneaux de consultation adaptés à votre emploi du temps. <a href='{{appointment_link}}'>En savoir plus</a>.</p><p>Prenez soin de vous,<br>Dr. Martin et l'équipe de prévention</p>",
            "<p>{{username}}, ne négligez pas votre santé!</p><p>Les dernières statistiques montrent l'importance de la prévention régulière. Notre {{campaign_title}} est spécialement conçue pour des personnes comme vous.</p><p><a href='{{appointment_link}}'>Prenez rendez-vous</a> dès aujourd'hui pour assurer votre bien-être à long terme.</p><p>À votre santé,<br>L'équipe de soins préventifs</p>",
            "<p>Bonjour {{username}},</p><p>Nous avons remarqué que vous n'avez pas effectué de {{campaign_title}} depuis un certain temps. Pour maintenir une bonne santé, nous vous recommandons vivement de planifier une visite.</p><p>Cliquez <a href='{{appointment_link}}'>ici</a> pour choisir un créneau qui vous convient.</p><p>Bien cordialement,<br>Service de prévention médicale</p>",
        ]

        sms_templates = [
            "Bonjour {{username}}, rappel important pour {{campaign_title}}. Pour votre santé, prenez RDV au plus vite: {{appointment_link}}",
            "{{username}}, {{campaign_title}} - Des créneaux sont disponibles cette semaine. Prenez soin de votre santé: {{appointment_link}}",
            "Santé: {{campaign_title}} - N'attendez pas pour agir. Cliquez pour RDV {{appointment_link}} ou répondez à ce message",
            "Important: Votre {{campaign_title}} est maintenant due. Réservez en ligne {{appointment_link}} ou appelez le 0123456789",
        ]

        # Create high-quality campaigns with strategic targeting
        for i in range(count):
            # Use predefined titles or create variations for extras
            if i < len(titles):
                title = titles[i]
            else:
                base_title = random.choice(titles)
                title = f"{base_title} - Phase {random.randint(2, 5)}"

            # Choose appropriate category based on title
            if "vaccination" in title.lower() or "vaccin" in title.lower():
                category_name = "Vaccination"
            elif "dépistage" in title.lower() or "cancer" in title.lower():
                category_name = "Dépistage"
            elif "prévention" in title.lower() or "risque" in title.lower():
                category_name = "Prévention"
            elif "suivi" in title.lower() or "chronique" in title.lower():
                category_name = "Suivi médical"
            elif "mental" in title.lower() or "stress" in title.lower():
                category_name = "Santé mentale"
            elif "activité" in title.lower() or "physique" in title.lower():
                category_name = "Activité physique"
            else:
                category_name = random.choice(["Prévention", "Dépistage", "Vaccination"])

            # Find the category object
            category = next(
                (c for c in categories if c.name == category_name),
                random.choice(categories),
            )

            # Campaign dates - seasonal patterns
            current_month = timezone.now().month

            # Vaccination campaigns often in fall/winter
            if category_name == "Vaccination":
                if current_month in [9, 10, 11, 12, 1, 2]:  # Fall/Winter
                    start_days = random.randint(-30, 30)  # Around now
                else:
                    start_days = random.randint(90, 180)  # Future campaign
            # Mental health often has peaks in winter
            elif category_name == "Santé mentale" and current_month in [11, 12, 1, 2]:
                start_days = random.randint(-20, 30)
            # Physical activity often pushed in spring
            elif category_name == "Activité physique" and current_month in [3, 4, 5]:
                start_days = random.randint(-30, 30)
            else:
                start_days = random.randint(-60, 120)

            # Campaign duration appropriate to type
            if category_name in ["Vaccination", "Dépistage"]:
                duration = random.randint(30, 90)  # Shorter, focused campaigns
            else:
                duration = random.randint(60, 180)  # Longer ongoing campaigns

            start_date = timezone.now() + timedelta(days=start_days)
            end_date = start_date + timedelta(days=duration)

            # Strategic targeting based on campaign type
            if "senior" in title.lower() or "âgé" in title.lower():
                target_age_groups = ["51-65", "65+"]
            elif (
                "jeune" in title.lower()
                or "adolescent" in title.lower()
                or "HPV" in title
            ):
                target_age_groups = ["0-18", "19-35"]
            elif "professionnel" in title.lower() or "travail" in title.lower():
                target_age_groups = ["19-35", "36-50"]
            else:
                # Sample based on campaign focus
                if category_name == "Vaccination":
                    weights = [
                        0.2,
                        0.15,
                        0.15,
                        0.2,
                        0.3,
                    ]  # Higher for youngest and oldest
                elif category_name == "Dépistage":
                    weights = [0.05, 0.15, 0.3, 0.3, 0.2]  # Higher for middle and older
                else:
                    weights = [0.2, 0.2, 0.2, 0.2, 0.2]  # Equal

                # Choose how many age groups to target (1-5)
                num_age_groups = random.choices(
                    [1, 2, 3, 4, 5], weights=[0.1, 0.3, 0.4, 0.15, 0.05]
                )[0]

                # Get all age groups
                all_age_groups = ["0-18", "19-35", "36-50", "51-65", "65+"]

                # Sample age groups with weights
                target_age_groups = random.choices(
                    all_age_groups, weights=weights, k=num_age_groups
                )
                target_age_groups = list(set(target_age_groups))  # Remove duplicates

            # Geographic targeting - often campaigns focus on specific regions
            if random.random() < 0.6:  # 60% chance of geographic focus
                # Choose how many locations (1-5)
                num_locations = random.choices(
                    [1, 2, 3, 4, 5], weights=[0.2, 0.3, 0.3, 0.15, 0.05]
                )[0]

                # Get main locations
                main_locations = [
                    "Paris",
                    "Lyon",
                    "Marseille",
                    "Bordeaux",
                    "Lille",
                    "Toulouse",
                    "Nantes",
                    "Strasbourg",
                    "Montreal",
                    "Algiers",
                ]

                target_locations = random.sample(main_locations, k=num_locations)
            else:
                # Broader campaigns
                all_locations = [
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
                ]
                # Sample 3-8 locations
                target_locations = random.sample(all_locations, k=random.randint(3, 8))

            # Language targeting matching regions
            if any(
                loc in ["Paris", "Lyon", "Marseille", "Bordeaux"]
                for loc in target_locations
            ):
                target_languages = ["fr"]
            elif any(loc in ["Montreal", "Quebec"] for loc in target_locations):
                target_languages = ["fr", "en"]
            elif any(loc in ["Brussels", "Geneva"] for loc in target_locations):
                target_languages = ["fr", "en", "de"]
            elif any(loc in ["Algiers", "Tunis", "Rabat"] for loc in target_locations):
                target_languages = ["fr", "ar"]
            else:
                target_languages = random.sample(
                    ["fr", "en", "ar", "es", "de"], k=random.randint(1, 3)
                )

            # Template selection based on campaign type
            if category_name in ["Vaccination", "Dépistage"]:
                # More urgent, direct templates
                email_template = random.choice(email_templates[:2])
                sms_template = random.choice(sms_templates[:2])
            else:
                # More informational templates
                email_template = random.choice(email_templates[2:])
                sms_template = random.choice(sms_templates[2:])

            # Create campaign with realistic attributes
            campaign = Campaign.objects.create(
                title=title,
                category=category,
                description=f"Description détaillée pour la campagne {title}, ciblant {', '.join(target_age_groups)} dans {', '.join(target_locations[:3])}{' et autres régions' if len(target_locations) > 3 else ''}.",
                start_date=start_date,
                end_date=end_date,
                is_active=start_date
                <= timezone.now()
                <= end_date,  # Active if current time falls within campaign dates
                target_age_groups=target_age_groups,
                target_locations=target_locations,
                target_languages=target_languages,
                email_template=email_template,
                sms_template=sms_template,
                created_by=random.choice(staff_users),
                updated_by=random.choice(staff_users),
            )

            campaigns.append(campaign)

        return campaigns


"""NOTE:
The code above generates a more realistic distribution of patients across different metropolitan areas. It uses a population-based approach to create a more meaningful geographic pattern in the ML model training. The campaign targeting is based on the patient's location, age group, and language preference, which will help the prediction models better understand how location correlates with patient behavior, response rates, and campaign effectiveness.
"""
