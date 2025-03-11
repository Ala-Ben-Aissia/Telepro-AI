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
            "age_groups": ["19-35", "36-50"],
            "locations": ["Montreal", "Quebec"],
            "gender": "F",
            "languages": ["fr", "en"],
            "has_active_consent": true
        }
        """
        criteria = (
            json.loads(criteria_json) if isinstance(criteria_json, str) else criteria_json
        )
        query = Q()

        # Build query based on criteria
        if criteria.get("age_groups"):
            query &= Q(age_group__in=criteria["age_groups"])

        if criteria.get("locations"):
            query &= Q(location__in=criteria["locations"])

        if criteria.get("gender"):
            query &= Q(gender=criteria["gender"])

        if criteria.get("languages"):
            query &= Q(language_preference__in=criteria["languages"])

        # Always respect consent
        query &= Q(has_active_consent=criteria.get("has_active_consent", True))

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
                l = lang["language_preference"] or "unknown"
                count = patients.filter(
                    language_preference=lang["language_preference"]
                ).count()
                stats["by_language"][l] = {
                    "count": count,
                    "percentage": round((count / total) * 100, 2),
                }

        return stats
