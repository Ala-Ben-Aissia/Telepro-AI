"""
Message Personalization Service

This service provides personalized message content based on patient preferences,
historical engagement, and campaign context.
"""

from django.utils import timezone
from django.template import Template, Context

from campaigns.models import Campaign, CommunicationLog
from patients.models import Patient


class PersonalizationService:
    """
    Service for personalizing message content based on patient data.

    This service:
    - Personalizes message templates with patient data
    - Suggests optimal message content based on historical engagement
    - Adapts message tone and style based on patient preferences
    """

    @staticmethod
    def personalize_message(template_content, patient_id, campaign_id=None):
        """
        Personalize a message template for a specific patient.

        Args:
            template_content: The message template content
            patient_id: ID of the patient
            campaign_id: Optional ID of the campaign

        Returns:
            Dictionary with personalized message
        """
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return {"status": "error", "message": "Patient not found"}

        # Get campaign if provided
        campaign = None
        if campaign_id:
            try:
                campaign = Campaign.objects.get(id=campaign_id)
            except Campaign.DoesNotExist:
                pass

        # Create context with patient data
        context_data = {
            "username": patient.user.username,
            "email": patient.user.email,
            "medical_record_number": patient.medical_record_number or "Not provided",
            "age_group": patient.age_group or "Not specified",
            "location": patient.location or "Not specified",
            "language": patient.language_preference or "Not specified",
            "preferred_contact": patient.preferred_contact_methods,
            "gender": patient.get_gender_display() if patient.gender else "Not specified",
            "current_date": timezone.now().strftime("%Y-%m-%d"),
            "current_time": timezone.now().strftime("%H:%M"),
        }

        # Add campaign data if available
        if campaign:
            context_data.update(
                {
                    "campaign_title": campaign.title,
                    "campaign_category": campaign.category.name
                    if campaign.category
                    else "General",
                    "campaign_start_date": campaign.start_date.strftime("%Y-%m-%d")
                    if campaign.start_date
                    else "",
                    "campaign_end_date": campaign.end_date.strftime("%Y-%m-%d")
                    if campaign.end_date
                    else "",
                }
            )

        # Add custom appointment link (in a real system, this would be generated dynamically)
        context_data["appointment_link"] = f"https://telepro.ai/appointments/{patient_id}"

        # Add doctor name (in a real system, this would be fetched from a database)
        context_data["doctor_name"] = "Dr. Smith"

        # Personalize the template
        try:
            # Replace Django-style variables ({{ var }})
            personalized_content = PersonalizationService._replace_django_variables(
                template_content, context_data
            )

            # Replace simple variables (%var%)
            personalized_content = PersonalizationService._replace_simple_variables(
                personalized_content, context_data
            )

            return {
                "status": "success",
                "original_template": template_content,
                "personalized_message": personalized_content,
                "patient_id": str(patient_id),
                "campaign_id": campaign_id,
                "variables_used": list(context_data.keys()),
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error personalizing message: {str(e)}",
            }

    @staticmethod
    def _replace_django_variables(template_content, context_data):
        """Replace Django-style variables ({{ var }}) in the template"""
        try:
            template = Template(template_content)
            context = Context(context_data)
            return template.render(context)
        except Exception:
            # Fall back to simple replacement if Django template fails
            return PersonalizationService._replace_simple_variables(
                template_content, context_data
            )

    @staticmethod
    def _replace_simple_variables(template_content, context_data):
        """Replace simple variables (%var%) in the template"""
        result = template_content

        # Replace each variable
        for key, value in context_data.items():
            if value is not None:
                # Replace both %var% and {{var}} formats
                result = result.replace(f"%{key}%", str(value))
                result = result.replace(f"{{{{{key}}}}}", str(value))

        return result

    @staticmethod
    def suggest_personalized_templates(campaign_id, patient_id=None):
        """
        Suggest personalized message templates for a campaign.

        Args:
            campaign_id: ID of the campaign
            patient_id: Optional ID of a specific patient

        Returns:
            Dictionary with template suggestions
        """
        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            return {"status": "error", "message": "Campaign not found"}

        # Get campaign category
        category = campaign.category.name if campaign.category else "General"

        # Base templates by category
        base_templates = {
            "Vaccination": {
                "email_subject": "Time for your {{campaign_category}} update",
                "email_body": """
Dear {{username}},

It's time for your {{campaign_category}} update.

Please click here to schedule your appointment: {{appointment_link}}

Best regards,
{{doctor_name}}
                """,
                "sms": "Hi {{username}}, it's time for your {{campaign_category}} update. Schedule here: {{appointment_link}}",
            },
            "Dental": {
                "email_subject": "Your dental check-up reminder",
                "email_body": """
Dear {{username}},

This is a friendly reminder that it's time for your dental check-up.

Please click here to schedule your appointment: {{appointment_link}}

Best regards,
{{doctor_name}}
                """,
                "sms": "Hi {{username}}, time for your dental check-up. Schedule here: {{appointment_link}}",
            },
            "Prévention": {
                "email_subject": "Important health prevention reminder",
                "email_body": """
Bonjour {{username}},

Nous vous rappelons l'importance de votre suivi de santé préventif.

Cliquez ici pour prendre rendez-vous: {{appointment_link}}

Cordialement,
{{doctor_name}}
                """,
                "sms": "Bonjour {{username}}, rappel de prévention santé. RDV: {{appointment_link}}",
            },
            "General": {
                "email_subject": "Your health reminder",
                "email_body": """
Dear {{username}},

This is a reminder about your upcoming health needs.

Please click here to schedule your appointment: {{appointment_link}}

Best regards,
{{doctor_name}}
                """,
                "sms": "Hi {{username}}, this is your health reminder. Schedule here: {{appointment_link}}",
            },
        }

        # Get templates for this category or fall back to General
        templates = base_templates.get(category, base_templates["General"])

        # If patient ID is provided, personalize the templates
        if patient_id:
            try:
                personalized_email_subject = PersonalizationService.personalize_message(
                    templates["email_subject"], patient_id, campaign_id
                )
                personalized_email_body = PersonalizationService.personalize_message(
                    templates["email_body"], patient_id, campaign_id
                )
                personalized_sms = PersonalizationService.personalize_message(
                    templates["sms"], patient_id, campaign_id
                )

                templates["email_subject"] = personalized_email_subject.get(
                    "personalized_message", templates["email_subject"]
                )
                templates["email_body"] = personalized_email_body.get(
                    "personalized_message", templates["email_body"]
                )
                templates["sms"] = personalized_sms.get(
                    "personalized_message", templates["sms"]
                )
            except Exception:
                # If personalization fails, use the base templates
                pass

        return {
            "status": "success",
            "campaign_id": campaign_id,
            "campaign_title": campaign.title,
            "category": category,
            "templates": templates,
            "personalized_for_patient": patient_id is not None,
            "patient_id": str(patient_id) if patient_id else None,
        }

    @staticmethod
    def analyze_message_effectiveness(campaign_id):
        """
        Analyze the effectiveness of different message templates.

        Args:
            campaign_id: ID of the campaign

        Returns:
            Dictionary with message effectiveness analysis
        """
        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            return {"status": "error", "message": "Campaign not found"}

        # Get communication logs for this campaign
        logs = CommunicationLog.objects.filter(campaign=campaign)

        if not logs.exists():
            return {
                "status": "error",
                "message": "No communication logs found for this campaign",
            }

        # Analyze by communication type
        email_logs = logs.filter(communication_type="EMAIL")
        sms_logs = logs.filter(communication_type="SMS")

        # Calculate effectiveness metrics
        email_metrics = PersonalizationService._calculate_effectiveness_metrics(
            email_logs
        )
        sms_metrics = PersonalizationService._calculate_effectiveness_metrics(sms_logs)

        # Overall metrics
        total_logs = logs.count()
        responded_logs = logs.filter(status="RESPONDED").count()
        read_logs = logs.filter(status="READ").count()

        overall_metrics = {
            "total": total_logs,
            "response_rate": responded_logs / total_logs if total_logs > 0 else 0,
            "read_rate": read_logs / total_logs if total_logs > 0 else 0,
        }

        return {
            "status": "success",
            "campaign_id": campaign_id,
            "campaign_title": campaign.title,
            "overall_metrics": overall_metrics,
            "email_metrics": email_metrics,
            "sms_metrics": sms_metrics,
            "recommendation": PersonalizationService._generate_message_recommendations(
                email_metrics, sms_metrics
            ),
        }

    @staticmethod
    def _calculate_effectiveness_metrics(logs):
        """Calculate effectiveness metrics for a set of communication logs"""
        total = logs.count()

        if total == 0:
            return {
                "total": 0,
                "response_rate": 0,
                "read_rate": 0,
                "average_time_to_response": 0,
            }

        responded = logs.filter(status="RESPONDED").count()
        read = logs.filter(status="READ").count()

        # Calculate average time to response
        avg_time = 0
        response_times = []

        for log in logs.filter(
            status="RESPONDED", sent_at__isnull=False, responded_at__isnull=False
        ):
            if log.sent_at and log.responded_at:
                time_diff = (
                    log.responded_at - log.sent_at
                ).total_seconds() / 3600  # hours
                response_times.append(time_diff)

        if response_times:
            avg_time = sum(response_times) / len(response_times)

        return {
            "total": total,
            "response_rate": responded / total if total > 0 else 0,
            "read_rate": read / total if total > 0 else 0,
            "average_time_to_response": avg_time,
        }

    @staticmethod
    def _generate_message_recommendations(email_metrics, sms_metrics):
        """Generate message recommendations based on metrics"""
        recommendations = []

        # Compare email vs SMS effectiveness
        if email_metrics["total"] > 0 and sms_metrics["total"] > 0:
            if email_metrics["response_rate"] > sms_metrics["response_rate"]:
                recommendations.append(
                    "Email messages have a higher response rate than SMS messages."
                )
            elif sms_metrics["response_rate"] > email_metrics["response_rate"]:
                recommendations.append(
                    "SMS messages have a higher response rate than email messages."
                )

            if (
                email_metrics["average_time_to_response"]
                < sms_metrics["average_time_to_response"]
            ):
                recommendations.append(
                    "Email messages receive faster responses than SMS messages."
                )
            elif (
                sms_metrics["average_time_to_response"]
                < email_metrics["average_time_to_response"]
            ):
                recommendations.append(
                    "SMS messages receive faster responses than email messages."
                )

        # General recommendations
        if email_metrics["response_rate"] < 0.2 and email_metrics["total"] > 10:
            recommendations.append(
                "Email response rate is low. Consider revising email templates."
            )

        if sms_metrics["response_rate"] < 0.2 and sms_metrics["total"] > 10:
            recommendations.append(
                "SMS response rate is low. Consider using shorter, more direct messages."
            )

        if not recommendations:
            recommendations.append("Message effectiveness is within expected ranges.")

        return recommendations

    @staticmethod
    def get_template_variables():
        """
        Get a list of available template variables.

        Returns:
            Dictionary with available template variables
        """
        variables = {
            "patient": [
                "username",
                "email",
                "medical_record_number",
                "age_group",
                "location",
                "language",
                "preferred_contact",
                "gender",
                "appointment_link",
            ],
            "campaign": [
                "campaign_title",
                "campaign_category",
                "campaign_start_date",
                "campaign_end_date",
            ],
            "date_time": ["current_date", "current_time"],
            "other": ["doctor_name"],
        }

        # Flatten for easy reference
        all_variables = []
        for category, vars in variables.items():
            all_variables.extend(vars)

        return {
            "status": "success",
            "variables_by_category": variables,
            "all_variables": all_variables,
            "usage_example": "Use {{variable_name}} in your templates, e.g., 'Hello {{username}}'",
        }
