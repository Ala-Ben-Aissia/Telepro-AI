import json

from django.db.models import Q

from patients.models import Patient


class SegmentationService:
    @staticmethod
    def get_patients_by_criteria(criteria_json):
        """
        Filter patients based on specified criteria

        criteria_json format:
        {
            "age_groups": ["19-35", "36-50"],  # or "age_group": ["19-35", "36-50"]
            "locations": ["Montreal", "Quebec"],  # or "location": ["Montreal", "Quebec"]
            "gender": "F",
            "languages": ["fr", "en"],  # or "language_preference": ["fr", "en"]
            "has_active_consent": true
        }
        """
        criteria = (
            json.loads(criteria_json) if isinstance(criteria_json, str) else criteria_json
        )
        query = Q()

        # Build query based on criteria - handle both plural and singular field names
        # Age group criteria
        if criteria.get("age_groups"):
            query &= Q(age_group__in=criteria["age_groups"])
        elif criteria.get("age_group"):
            query &= Q(age_group__in=criteria["age_group"])

        # Location criteria
        if criteria.get("locations"):
            query &= Q(location__in=criteria["locations"])
        elif criteria.get("location"):
            query &= Q(location__in=criteria["location"])

        # Gender criteria
        if criteria.get("gender"):
            query &= Q(gender=criteria["gender"])

        # Language criteria
        if criteria.get("languages"):
            query &= Q(language_preference__in=criteria["languages"])
        elif criteria.get("language_preference"):
            query &= Q(language_preference__in=criteria["language_preference"])

        # Engagement score criteria (for advanced filtering)
        if criteria.get("engagement_score__gt"):
            query &= Q(engagement_score__gt=criteria["engagement_score__gt"])
        elif criteria.get("engagement_score__lt"):
            query &= Q(engagement_score__lt=criteria["engagement_score__lt"])
        elif criteria.get("engagement_score__gte"):
            query &= Q(engagement_score__gte=criteria["engagement_score__gte"])
        elif criteria.get("engagement_score__lte"):
            query &= Q(engagement_score__lte=criteria["engagement_score__lte"])

        # Patient IDs criteria (for specific targeting)
        if criteria.get("patient_ids"):
            query &= Q(id__in=criteria["patient_ids"])

        # Always respect consent unless explicitly set to False
        if criteria.get("has_active_consent") is not False:
            query &= Q(has_active_consent=True)

        # Return filtered queryset
        return Patient.objects.filter(query)

    @staticmethod
    def get_segment_patient_count(segment):
        """Get count of patients matching segment criteria"""
        try:
            patients = SegmentationService.get_patients_by_criteria(segment.criteria)
            return patients.count()
        except Exception as e:
            print(f"Error counting segment patients: {str(e)}")
            return 0

    @staticmethod
    def update_segment_statistics(segment):
        """Update a segment with statistics about the patients that match"""
        patients = SegmentationService.get_patients_by_criteria(segment.criteria)
        total = patients.count()

        # Get some basic statistics
        stats = {
            "total_patients": total,
            "by_age_group": {},
            "by_gender": {},
            "by_language": {},
        }

        # Only calculate if we have patients
        if total > 0:
            # Age group breakdown
            for age_group in patients.values("age_group").distinct():
                group = age_group["age_group"] or "unknown"
                count = patients.filter(age_group=age_group["age_group"]).count()
                stats["by_age_group"][group] = {
                    "count": count,
                    "percentage": round((count / total) * 100, 2),
                }

            # Gender breakdown
            for gender in patients.values("gender").distinct():
                g = gender["gender"] or "unknown"
                count = patients.filter(gender=gender["gender"]).count()
                stats["by_gender"][g] = {
                    "count": count,
                    "percentage": round((count / total) * 100, 2),
                }

            # Language breakdown
            for lang in patients.values("language_preference").distinct():
                l = lang["language_preference"] or "unknown"  # noqa: E741
                count = patients.filter(
                    language_preference=lang["language_preference"]
                ).count()
                stats["by_language"][l] = {
                    "count": count,
                    "percentage": round((count / total) * 100, 2),
                }

        return stats
