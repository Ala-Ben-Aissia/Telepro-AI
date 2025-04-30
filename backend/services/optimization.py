"""
Campaign Optimization Service

This service integrates segmentation, prediction, and campaign execution
to provide optimized campaign targeting and content suggestions.
"""

from django.utils import timezone

from campaigns.models import Campaign, PatientSegment
from services.ai.clustering import PatientClusteringService
from services.ai.prediction import CampaignPredictionService
from services.segmentation import SegmentationService


class CampaignOptimizationService:
    """
    Service for optimizing campaigns using AI/ML techniques.

    This service integrates:
    - Patient segmentation (both rule-based and ML-driven)
    - Response prediction
    - Message optimization
    - Sending time optimization
    """

    @staticmethod
    def optimize_campaign(campaign_id):
        """
        Generate optimization suggestions for a campaign.

        Args:
            campaign_id: ID of the campaign to optimize

        Returns:
            Dictionary with optimization suggestions
        """
        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            return {"status": "error", "message": "Campaign not found"}

        # Get basic campaign effectiveness prediction
        effectiveness = CampaignPredictionService.predict_campaign_effectiveness(
            campaign_id
        )

        # Generate ML-driven segments
        ml_segments = CampaignOptimizationService._generate_ml_segments(campaign)

        # Get sending time suggestions
        timing_suggestions = CampaignOptimizationService._suggest_sending_times(campaign)

        # Get message content suggestions
        content_suggestions = CampaignOptimizationService._suggest_message_content(
            campaign
        )

        return {
            "status": "success",
            "campaign_id": campaign_id,
            "campaign_title": campaign.title,
            "predicted_effectiveness": effectiveness,
            "ml_segments": ml_segments,
            "timing_suggestions": timing_suggestions,
            "content_suggestions": content_suggestions,
        }

    @staticmethod
    def _generate_ml_segments(campaign):
        """
        Generate ML-driven segments for a campaign using clustering.

        Args:
            campaign: Campaign object

        Returns:
            List of suggested segments
        """
        # Use the PatientClusteringService to generate clusters
        clustering_results = PatientClusteringService.cluster_patients(
            algorithm="kmeans",
            n_clusters=3,  # Start with 3 clusters
            include_only_with_consent=True,
        )

        if "clusters" not in clustering_results:
            return []

        # Convert clusters to segments
        suggested_segments = []
        for cluster_name, cluster_data in clustering_results["clusters"].items():
            if cluster_data.get("is_noise", False):
                continue  # Skip noise clusters

            # Create a segment suggestion
            segment_suggestion = {
                "name": f"{campaign.title} - {cluster_name}",
                "description": f"ML-generated segment based on {cluster_name}",
                "patient_count": cluster_data.get("count", 0),
                "patient_ids": cluster_data.get("patient_ids", []),
                "features": cluster_data.get("top_features", []),
                "already_exists": False,  # Will be set to True if a similar segment exists
            }

            # Check if a similar segment already exists
            existing_segments = PatientSegment.objects.filter(
                name__contains=cluster_name, campaigns=campaign
            )
            if existing_segments.exists():
                segment_suggestion["already_exists"] = True
                segment_suggestion["existing_segment_id"] = existing_segments.first().id

            suggested_segments.append(segment_suggestion)

        return suggested_segments

    @staticmethod
    def _suggest_sending_times(campaign):
        """
        Suggest optimal sending times for a campaign.

        Args:
            campaign: Campaign object

        Returns:
            Dictionary with sending time suggestions
        """
        # Get current time
        now = timezone.now()

        # Default suggestions based on general best practices
        default_suggestions = {
            "weekdays": ["Tuesday", "Wednesday", "Thursday"],
            "weekend": ["Saturday"],
            "times": {"morning": "10:00", "afternoon": "14:00", "evening": "19:00"},
            "best_overall": "Wednesday at 14:00",
        }

        # Adjust based on campaign category if available
        category_name = "General"
        if campaign.category:
            category_name = campaign.category.name.lower()

            # Customize timing based on category
            if category_name == "vaccination":
                # Vaccinations often better in morning
                default_suggestions["times"]["morning"] = "09:00"
                default_suggestions["best_overall"] = "Tuesday at 09:00"
            elif category_name == "dental":
                # Dental appointments often better in afternoon
                default_suggestions["times"]["afternoon"] = "15:00"
                default_suggestions["best_overall"] = "Thursday at 15:00"

        # In a real implementation, you would analyze historical data
        # to determine the best sending times for this specific campaign type

        # Calculate next optimal time based on current time and best_overall day
        best_day = default_suggestions["best_overall"].split(" at ")[0]
        best_time = default_suggestions["best_overall"].split(" at ")[1]
        best_hour = int(best_time.split(":")[0])
        best_minute = int(best_time.split(":")[1])

        # Map day name to weekday number (0=Monday, 6=Sunday)
        day_mapping = {
            "Monday": 0,
            "Tuesday": 1,
            "Wednesday": 2,
            "Thursday": 3,
            "Friday": 4,
            "Saturday": 5,
            "Sunday": 6,
        }

        # Calculate days to add to get to the next occurrence of best_day
        current_weekday = now.weekday()
        target_weekday = day_mapping.get(
            best_day, 2
        )  # Default to Wednesday (2) if not found
        days_to_add = (target_weekday - current_weekday) % 7
        if days_to_add == 0 and now.hour >= best_hour:
            days_to_add = (
                7  # If today is the target day but we've passed the time, go to next week
            )

        next_optimal = now + timezone.timedelta(days=days_to_add)
        next_optimal = next_optimal.replace(hour=best_hour, minute=best_minute, second=0)

        return {
            "based_on": f"campaign_category_{category_name}",
            "suggestions": default_suggestions,
            "next_optimal_time": next_optimal.isoformat(),
            "campaign_start": campaign.start_date.isoformat()
            if campaign.start_date
            else None,
            "campaign_end": campaign.end_date.isoformat() if campaign.end_date else None,
        }

    @staticmethod
    def _suggest_message_content(campaign):
        """
        Suggest optimized message content for a campaign.

        Args:
            campaign: Campaign object

        Returns:
            Dictionary with message content suggestions
        """
        # Get campaign category
        category = "General"
        if campaign.category:
            category = campaign.category.name

        # Default suggestions based on campaign category
        suggestions = {
            "subject_lines": [
                f"Important health update about {category}",
                f"Your {category} reminder",
                f"Don't forget: {category} follow-up",
            ],
            "greeting_options": [
                "Hello {{first_name}}",
                "Dear {{first_name}}",
                "Bonjour {{first_name}}",
            ],
            "call_to_action": [
                "Schedule your appointment today",
                "Click here to learn more",
                "Respond to confirm your availability",
            ],
        }

        # Add category-specific suggestions
        if category.lower() == "vaccination":
            suggestions["subject_lines"].extend(
                [
                    "Protect yourself: Vaccination reminder",
                    "Time for your vaccination update",
                ]
            )
            suggestions["call_to_action"].extend(
                ["Book your vaccination appointment", "Check your vaccination status"]
            )
        elif category.lower() == "dental":
            suggestions["subject_lines"].extend(
                [
                    "Time for your dental check-up",
                    "Smile brighter: Dental appointment reminder",
                ]
            )
            suggestions["call_to_action"].extend(
                ["Book your dental check-up", "Schedule your cleaning appointment"]
            )

        # In a real implementation, you would analyze historical data
        # to determine the most effective message content for this campaign type

        # For now, return default suggestions
        return {
            "based_on": "campaign_category",
            "category": category,
            "suggestions": suggestions,
            "template_variables": [
                "first_name",
                "last_name",
                "appointment_link",
                "doctor_name",
            ],
        }

    @staticmethod
    def apply_optimization(campaign_id, optimization_data):
        """
        Apply optimization suggestions to a campaign.

        Args:
            campaign_id: ID of the campaign to optimize
            optimization_data: Dictionary with optimization choices

        Returns:
            Updated campaign data
        """
        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            return {"status": "error", "message": "Campaign not found"}

        # Apply ML segments if requested
        if optimization_data.get("apply_ml_segments"):
            segment_ids = optimization_data.get("selected_segment_ids", [])

            # Create new segments if needed
            if optimization_data.get("create_new_segments"):
                new_segments = CampaignOptimizationService._create_ml_segments(
                    campaign, optimization_data.get("new_segments", [])
                )
                segment_ids.extend([s.id for s in new_segments])

            # Link segments to campaign
            for segment_id in segment_ids:
                try:
                    segment = PatientSegment.objects.get(id=segment_id)
                    campaign.segments.add(segment)
                except PatientSegment.DoesNotExist:
                    continue

        # Apply timing optimization if requested
        if optimization_data.get("apply_timing_optimization"):
            # Update campaign start date if provided
            if optimization_data.get("start_date"):
                campaign.start_date = optimization_data.get("start_date")

            # In a real implementation, you would also update scheduled sending times

        # Apply content optimization if requested
        if optimization_data.get("apply_content_optimization"):
            # Update email template if provided
            if optimization_data.get("email_template"):
                campaign.email_template = optimization_data.get("email_template")

            # Update SMS template if provided
            if optimization_data.get("sms_template"):
                campaign.sms_template = optimization_data.get("sms_template")

        # Save changes
        campaign.save()

        return {
            "status": "success",
            "campaign_id": campaign_id,
            "message": "Campaign optimization applied successfully",
        }

    @staticmethod
    def _create_ml_segments(campaign, segment_data_list):
        """
        Create new ML-driven segments for a campaign.

        Args:
            campaign: Campaign object
            segment_data_list: List of segment data dictionaries

        Returns:
            List of created PatientSegment objects
        """
        created_segments = []

        for segment_data in segment_data_list:
            # Create criteria JSON
            criteria = {"patient_ids": segment_data.get("patient_ids", [])}

            # Create the segment
            segment = PatientSegment.objects.create(
                name=segment_data.get(
                    "name", f"ML Segment - {timezone.now().isoformat()}"
                ),
                description=segment_data.get("description", "ML-generated segment"),
                criteria=criteria,
                is_active=True,
            )

            # Link to campaign
            segment.campaigns.add(campaign)
            created_segments.append(segment)

        return created_segments
