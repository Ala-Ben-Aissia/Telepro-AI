from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime

from campaigns.models import Campaign  # Adapter l'import en fonction de ton app


class Command(BaseCommand):
    help = "Populate the Campaign model with initial data."

    def handle(self, *args, **options):
        campaigns_data = [
            {
                "title": "Vaccination Grippe Saisonnière",
                "category": 1,
                "description": "Campagne visant à encourager les populations vulnérables à se faire vacciner contre la grippe.",
                "start_date": "2025-10-01T08:00:00Z",
                "end_date": "2026-01-31T23:59:59Z",
                "is_active": True,
                "target_age_groups": ["60+", "Personnes à risque"],
                "target_locations": ["France", "Belgique", "Canada"],
                "target_languages": ["fr", "en"],
                "email_template": (
                    "<html><body>"
                    "<p>Bonjour {{username}},</p>"
                    "<p>La vaccination contre la grippe est essentielle pour votre santé. "
                    "Veuillez prendre rendez-vous dès aujourd'hui en cliquant sur "
                    "<a href='{{appointment_link}}'>ce lien</a>.</p>"
                    "<p>Cordialement,</p>"
                    "<p>L'équipe de santé</p>"
                    "</body></html>"
                ),
                "sms_template": "Bonjour {{username}}, n'oubliez pas de vous faire vacciner contre la grippe. RDV: {{appointment_link}}.",
            },
            {
                "title": "Dépistage du Diabète",
                "category": 2,
                "description": "Sensibilisation au dépistage précoce du diabète pour éviter les complications.",
                "start_date": "2025-03-01T08:00:00Z",
                "end_date": "2025-06-30T23:59:59Z",
                "is_active": True,
                "target_age_groups": ["40-60", "60+"],
                "target_locations": ["Tunisie", "Maroc", "Algérie"],
                "target_languages": ["fr", "ar"],
                "email_template": (
                    "<html><body>"
                    "<p>Bonjour {{username}},</p>"
                    "<p>Il est temps de vérifier votre glycémie pour un dépistage précoce du diabète. "
                    "Cliquez ici pour planifier votre test : "
                    "<a href='{{test_link}}'>Prendre Rendez-vous</a>.</p>"
                    "<p>Bien cordialement,</p>"
                    "<p>Votre Centre de Santé</p>"
                    "</body></html>"
                ),
                "sms_template": "Cher {{username}}, dépistage du diabète disponible. RDV: {{test_link}}.",
            },
            {
                "title": "Suivi des Patients Hypertendus",
                "category": 2,
                "description": "Programme de suivi et rappels pour les patients souffrant d'hypertension.",
                "start_date": "2025-04-15T08:00:00Z",
                "end_date": "2025-12-31T23:59:59Z",
                "is_active": False,
                "target_age_groups": ["40-60", "60+"],
                "target_locations": ["Égypte", "Liban"],
                "target_languages": ["ar", "fr"],
                "email_template": (
                    "<html><body>"
                    "<p>Bonjour {{username}},</p>"
                    "<p>Il est important de suivre votre tension. Veuillez consulter votre médecin et vérifier vos résultats via "
                    "<a href='{{followup_link}}'>votre espace patient</a>.</p>"
                    "<p>Merci,</p>"
                    "<p>L'équipe médicale</p>"
                    "</body></html>"
                ),
                "sms_template": "Cher {{username}}, pensez à vérifier votre tension. Suivez vos conseils ici: {{followup_link}}.",
            },
            {
                "title": "Campagne Prévention COVID-19",
                "category": 1,
                "description": "Rappels sur les gestes barrières et la vaccination contre le COVID-19.",
                "start_date": "2025-09-01T08:00:00Z",
                "end_date": "2026-02-28T23:59:59Z",
                "is_active": True,
                "target_age_groups": ["Tous"],
                "target_locations": ["Monde entier"],
                "target_languages": ["fr", "en", "es", "ar"],
                "email_template": (
                    "<html><body>"
                    "<p>Bonjour {{username}},</p>"
                    "<p>Restez informé et protégé contre le COVID-19. Consultez les dernières recommandations et prenez rendez-vous pour votre rappel vaccinal via "
                    "<a href='{{covid_link}}'>ce lien</a>.</p>"
                    "<p>Merci,</p>"
                    "<p>L'équipe de prévention</p>"
                    "</body></html>"
                ),
                "sms_template": "Cher {{username}}, protégez-vous contre le COVID-19. Plus d'infos: {{covid_link}}.",
            },
            {
                "title": "Santé Dentaire – Rappels de Consultation",
                "category": 2,
                "description": "Encouragement aux consultations dentaires régulières pour prévenir les problèmes bucco-dentaires.",
                "start_date": "2025-07-01T08:00:00Z",
                "end_date": "2026-07-01T23:59:59Z",
                "is_active": True,
                "target_age_groups": ["Tous"],
                "target_locations": ["France", "Belgique", "Canada"],
                "target_languages": ["fr", "en"],
                "email_template": (
                    "<html><body>"
                    "<p>Bonjour {{username}},</p>"
                    "<p>Un sourire sain commence par des visites régulières chez le dentiste. Planifiez votre consultation en cliquant sur "
                    "<a href='{{dental_link}}'>ce lien</a>.</p>"
                    "<p>Merci,</p>"
                    "<p>Votre cabinet dentaire</p>"
                    "</body></html>"
                ),
                "sms_template": "Cher {{username}}, pensez à votre rendez-vous dentaire. RDV: {{dental_link}}.",
            },
            {
                "title": "Sensibilisation au Cancer du Sein",
                "category": 3,
                "description": "Campagne de sensibilisation sur l'importance du dépistage du cancer du sein.",
                "start_date": "2025-10-01T08:00:00Z",
                "end_date": "2025-11-30T23:59:59Z",
                "is_active": True,
                "target_age_groups": ["40-60", "60+"],
                "target_locations": ["France", "Tunisie", "Maroc", "Algérie"],
                "target_languages": ["fr", "ar"],
                "email_template": (
                    "<html><body>"
                    "<p>Bonjour {{username}},</p>"
                    "<p>Le dépistage du cancer du sein peut sauver des vies. Prenez rendez-vous pour une mammographie en suivant "
                    "<a href='{{screening_link}}'>ce lien</a>.</p>"
                    "<p>Bien à vous,</p>"
                    "<p>Votre équipe de dépistage</p>"
                    "</body></html>"
                ),
                "sms_template": "Cher {{username}}, dépistage du cancer du sein disponible. RDV: {{screening_link}}.",
            },
            {
                "title": "Prévention des Maladies Cardiaques",
                "category": 3,
                "description": "Encouragement à adopter un mode de vie sain pour réduire les risques de maladies cardiovasculaires.",
                "start_date": "2025-05-01T08:00:00Z",
                "end_date": "2025-12-31T23:59:59Z",
                "is_active": False,
                "target_age_groups": ["40-60", "60+"],
                "target_locations": ["Monde entier"],
                "target_languages": ["fr", "en", "es"],
                "email_template": (
                    "<html><body>"
                    "<p>Bonjour {{username}},</p>"
                    "<p>Adoptez un mode de vie sain pour protéger votre cœur. Découvrez nos conseils et planifiez une consultation sur "
                    "<a href='{{heart_link}}'>votre espace santé</a>.</p>"
                    "<p>Bien cordialement,</p>"
                    "<p>L'équipe Cardio</p>"
                    "</body></html>"
                ),
                "sms_template": "Cher {{username}}, pour la santé de votre cœur, consultez vos conseils ici: {{heart_link}}.",
            },
        ]

        for data in campaigns_data:
            campaign, created = Campaign.objects.update_or_create(
                title=data["title"],
                defaults={
                    "category_id": data["category"],
                    "description": data["description"],
                    "start_date": parse_datetime(data["start_date"]),
                    "end_date": parse_datetime(data["end_date"]),
                    "is_active": data["is_active"],
                    "target_age_groups": data["target_age_groups"],
                    "target_locations": data["target_locations"],
                    "target_languages": data["target_languages"],
                    "email_template": data["email_template"],
                    "sms_template": data["sms_template"],
                },
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Campaign '{campaign.title}' created.")
                )
            else:
                self.stdout.write(f"Campaign '{campaign.title}' updated.")
