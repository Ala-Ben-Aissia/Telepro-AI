"""
ML-Driven Segmentation Service

This service provides advanced patient segmentation using machine learning techniques.
It integrates clustering algorithms with campaign targeting to create more effective segments.
"""

from django.utils import timezone
from django.db import models

from campaigns.models import Campaign, PatientSegment
from services.ai.clustering import PatientClusteringService
from services.segmentation import SegmentationService


class MLSegmentationService:
    """
    Service for creating and managing ML-driven patient segments.

    This service:
    - Creates segments based on clustering algorithms
    - Analyzes segment characteristics
    - Provides segment recommendations for campaigns
    - Integrates with campaign targeting
    """

    @staticmethod
    def create_ml_segments(algorithm="kmeans", n_clusters=3, name_prefix="ML Segment"):
        """
        Create ML-driven segments using clustering algorithms.

        Args:
            algorithm: Clustering algorithm to use ("kmeans" or "dbscan")
            n_clusters: Number of clusters to create (for KMeans)
            name_prefix: Prefix for segment names

        Returns:
            Dictionary with created segments information
        """
        # Use PatientClusteringService to generate clusters
        clustering_results = PatientClusteringService.cluster_patients(
            algorithm=algorithm, n_clusters=n_clusters, include_only_with_consent=True
        )

        if "clusters" not in clustering_results:
            return {
                "status": "error",
                "message": clustering_results.get("message", "Clustering failed"),
            }

        # Create segments from clusters
        created_segments = []
        for cluster_name, cluster_data in clustering_results["clusters"].items():
            if cluster_data.get("is_noise", False):
                continue  # Skip noise clusters

            # Create segment name with timestamp for uniqueness
            timestamp = timezone.now().strftime("%d/%m/%Y_%H%M")
            segment_name = f"{name_prefix} {cluster_name} ({timestamp})"

            # Create criteria JSON - use patient_ids for precise targeting
            criteria = {"patient_ids": cluster_data.get("patient_ids", [])}

            # Create segment description based on cluster characteristics
            description = f"ML-generated segment based on {algorithm.upper()} clustering"
            if "centroid" in cluster_data:
                description += f". Cluster size: {cluster_data.get('count', 0)} patients"

            # Create the segment
            try:
                segment = PatientSegment.objects.create(
                    name=segment_name,
                    description=description,
                    criteria=criteria,
                    is_active=True,
                )

                # Add segment metadata
                created_segments.append(
                    {
                        "id": segment.id,
                        "name": segment.name,
                        "description": segment.description,
                        "patient_count": cluster_data.get("count", 0),
                        "algorithm": algorithm,
                        "cluster_name": cluster_name,
                    }
                )
            except Exception as e:
                return {"status": "error", "message": f"Error creating segment: {str(e)}"}

        return {
            "status": "success",
            "segments_created": len(created_segments),
            "segments": created_segments,
        }

    @staticmethod
    def analyze_segment(segment_id):
        """
        Analyze a segment to extract key characteristics and patterns.

        Args:
            segment_id: ID of the segment to analyze

        Returns:
            Dictionary with segment analysis
        """
        try:
            segment = PatientSegment.objects.get(id=segment_id)
        except PatientSegment.DoesNotExist:
            return {"status": "error", "message": "Segment not found"}

        # Get patients in this segment
        patients = SegmentationService.get_patients_by_criteria(segment.criteria)

        if not patients.exists():
            return {"status": "error", "message": "No patients found in this segment"}

        # Get basic statistics
        stats = SegmentationService.update_segment_statistics(segment)

        # Calculate engagement metrics
        engagement_metrics = {
            "avg_engagement_score": patients.aggregate(
                avg_score=models.Avg("engagement_score")
            )["avg_score"]
            or 0,
            "high_engagement_count": patients.filter(engagement_score__gte=0.7).count(),
            "medium_engagement_count": patients.filter(
                engagement_score__gte=0.4, engagement_score__lt=0.7
            ).count(),
            "low_engagement_count": patients.filter(engagement_score__lt=0.4).count(),
        }

        # Calculate communication preferences
        communication_prefs = {
            "email": patients.filter(preferred_contact_method="EMAIL").count(),
            "sms": patients.filter(preferred_contact_method="SMS").count(),
            "call": patients.filter(preferred_contact_method="CALL").count(),
            "none": patients.filter(preferred_contact_method="NONE").count(),
        }

        # Get campaign response history if available
        from campaigns.models import CommunicationLog

        campaign_history = {}
        for campaign in Campaign.objects.filter(segments=segment):
            logs = CommunicationLog.objects.filter(
                campaign=campaign, patient__in=patients
            )

            if logs.exists():
                total = logs.count()
                responded = logs.filter(status="RESPONDED").count()
                read = logs.filter(status="READ").count()

                campaign_history[campaign.id] = {
                    "campaign_name": campaign.title,
                    "total_communications": total,
                    "response_rate": responded / total if total > 0 else 0,
                    "read_rate": read / total if total > 0 else 0,
                }

        return {
            "status": "success",
            "segment_id": segment_id,
            "segment_name": segment.name,
            "patient_count": patients.count(),
            "basic_stats": stats,
            "engagement_metrics": engagement_metrics,
            "communication_preferences": communication_prefs,
            "campaign_history": campaign_history,
        }

    @staticmethod
    def recommend_segments_for_campaign(campaign_id):
        """
        Recommend existing segments for a campaign based on targeting criteria.

        Args:
            campaign_id: ID of the campaign

        Returns:
            Dictionary with segment recommendations
        """
        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            return {"status": "error", "message": "Campaign not found"}

        # Get all active segments
        all_segments = PatientSegment.objects.filter(is_active=True)

        # Calculate segment match scores
        segment_scores = []

        for segment in all_segments:
            # Skip segments already linked to this campaign
            if campaign in segment.campaigns.all():
                continue

            # Get patients in this segment
            patients = SegmentationService.get_patients_by_criteria(segment.criteria)

            if not patients.exists():
                continue

            # Calculate match score based on campaign targeting criteria
            match_score = 0
            total_weight = 0

            # Check age group match
            if campaign.target_age_groups:
                total_weight += 0.3
                age_match_count = patients.filter(
                    age_group__in=campaign.target_age_groups
                ).count()
                age_match_score = (
                    age_match_count / patients.count() if patients.count() > 0 else 0
                )
                match_score += 0.3 * age_match_score

            # Check location match
            if campaign.target_locations:
                total_weight += 0.3
                location_match_count = patients.filter(
                    location__in=campaign.target_locations
                ).count()
                location_match_score = (
                    location_match_count / patients.count() if patients.count() > 0 else 0
                )
                match_score += 0.3 * location_match_score

            # Check language match
            if campaign.target_languages:
                total_weight += 0.2
                language_match_count = patients.filter(
                    language_preference__in=campaign.target_languages
                ).count()
                language_match_score = (
                    language_match_count / patients.count() if patients.count() > 0 else 0
                )
                match_score += 0.2 * language_match_score

            # Check engagement score (prefer engaged patients)
            total_weight += 0.2
            high_engagement_count = patients.filter(engagement_score__gte=0.5).count()
            engagement_score = (
                high_engagement_count / patients.count() if patients.count() > 0 else 0
            )
            match_score += 0.2 * engagement_score

            # Normalize score if we have weights
            if total_weight > 0:
                match_score = match_score / total_weight

            # Add to results
            segment_scores.append(
                {
                    "segment_id": segment.id,
                    "segment_name": segment.name,
                    "match_score": match_score,
                    "patient_count": patients.count(),
                    "description": segment.description,
                }
            )

        # Sort by match score
        segment_scores.sort(key=lambda x: x["match_score"], reverse=True)

        # Return top recommendations
        return {
            "status": "success",
            "campaign_id": campaign_id,
            "campaign_title": campaign.title,
            "recommended_segments": segment_scores[:5],  # Top 5 recommendations
            "total_segments_available": len(segment_scores),
        }

    @staticmethod
    def link_segment_to_campaign(segment_id, campaign_id):
        """
        Link a segment to a campaign.

        Args:
            segment_id: ID of the segment
            campaign_id: ID of the campaign

        Returns:
            Dictionary with result
        """
        try:
            segment = PatientSegment.objects.get(id=segment_id)
            campaign = Campaign.objects.get(id=campaign_id)
        except PatientSegment.DoesNotExist:
            return {"status": "error", "message": "Segment not found"}
        except Campaign.DoesNotExist:
            return {"status": "error", "message": "Campaign not found"}

        # Link segment to campaign
        campaign.segments.add(segment)

        return {
            "status": "success",
            "message": f"Segment '{segment.name}' linked to campaign '{campaign.title}'",
            "segment_id": segment_id,
            "campaign_id": campaign_id,
        }

    @staticmethod
    def get_segment_patients(segment_id, limit=100):
        """
        Get patients in a segment with detailed information.

        Args:
            segment_id: ID of the segment
            limit: Maximum number of patients to return

        Returns:
            Dictionary with patients information
        """
        try:
            segment = PatientSegment.objects.get(id=segment_id)
        except PatientSegment.DoesNotExist:
            return {"status": "error", "message": "Segment not found"}

        # Get patients in this segment
        patients = SegmentationService.get_patients_by_criteria(segment.criteria)

        if not patients.exists():
            return {"status": "error", "message": "No patients found in this segment"}

        # Limit the number of patients returned
        patients = patients[:limit]

        # Format patient data
        patient_data = []
        for patient in patients:
            patient_data.append(
                {
                    "id": str(patient.id),
                    "gender": patient.gender,
                    "age_group": patient.age_group,
                    "location": patient.location,
                    "language": patient.language_preference,
                    "engagement_score": patient.engagement_score,
                    "preferred_contact": patient.preferred_contact_method,
                    "email_verified": patient.email_verified,
                    "phone_verified": patient.phone_verified,
                    "has_consent": patient.has_active_consent,
                }
            )

        return {
            "status": "success",
            "segment_id": segment_id,
            "segment_name": segment.name,
            "total_patients": patients.count(),
            "patients": patient_data,
            "limit_applied": limit < patients.count(),
        }
