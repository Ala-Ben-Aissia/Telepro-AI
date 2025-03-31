from django.db.models import Avg, Count
from sklearn.cluster import KMeans
from sklearn.discriminant_analysis import StandardScaler

from services.ai.preprocessing import DataPreprocessingService


class PatientClusteringService:
    """
    Service for clustering patients based on their features.
    Uses machine learning to identify natural groupings of patients.
    """

    @staticmethod
    def cluster_patients(n_clusters=5, include_only_with_consent=True):
        """
        Cluster patients based on their features.

        Args:
            n_clusters: Number of clusters to create
            include_only_with_consent: Whether to only include patients with active consent

        Returns:
            Dictionary mapping cluster names to lists of patient IDs, and cluster characteristics
        """
        # Get preprocessed patient features
        features, patient_ids = DataPreprocessingService.extract_patient_features(
            include_only_with_consent=include_only_with_consent
        )

        if features is None or len(features) < n_clusters:
            return {
                "status": "insufficient_data",
                "message": f"Not enough patient data for clustering into {n_clusters} groups.",
            }

        # Standardize features
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)

        # Apply K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(features_scaled)

        # Prepare results
        clusters = {}
        for i in range(n_clusters):
            cluster_name = f"Cluster_{i + 1}"
            clusters[cluster_name] = {
                "patient_ids": [
                    patient_ids[j]
                    for j in range(len(patient_ids))
                    if cluster_labels[j] == i
                ],
                "count": sum(1 for label in cluster_labels if label == i),
                "centroid": kmeans.cluster_centers_[i].tolist(),
            }

        # Add cluster characteristics
        from patients.models import Patient

        for cluster_name, cluster_data in clusters.items():
            patient_ids = cluster_data["patient_ids"]
            if not patient_ids:
                continue

            # Get patients in this cluster
            cluster_patients = Patient.objects.filter(id__in=patient_ids)

            # Calculate cluster characteristics
            characteristics = {}

            # Age group distribution
            age_counts = dict(
                cluster_patients.values("age_group")
                .annotate(count=Count("id"))
                .values_list("age_group", "count")
            )

            top_age_group = (
                max(age_counts.items(), key=lambda x: x[1])[0] if age_counts else None
            )
            characteristics["top_age_group"] = top_age_group

            # Gender distribution
            gender_counts = dict(
                cluster_patients.values("gender")
                .annotate(count=Count("id"))
                .values_list("gender", "count")
            )

            top_gender = (
                max(gender_counts.items(), key=lambda x: x[1])[0]
                if gender_counts
                else None
            )
            characteristics["top_gender"] = top_gender

            # Location distribution
            location_counts = dict(
                cluster_patients.values("location")
                .annotate(count=Count("id"))
                .values_list("location", "count")
            )

            top_locations = sorted(
                location_counts.items(), key=lambda x: x[1], reverse=True
            )[:3]
            characteristics["top_locations"] = [
                loc for loc, count in top_locations if loc
            ]

            # Contact method preference
            contact_counts = dict(
                cluster_patients.values("preferred_contact_method")
                .annotate(count=Count("id"))
                .values_list("preferred_contact_method", "count")
            )

            top_contact = (
                max(contact_counts.items(), key=lambda x: x[1])[0]
                if contact_counts
                else None
            )
            characteristics["preferred_contact_method"] = top_contact

            # Average engagement score
            avg_engagement = (
                cluster_patients.aggregate(avg=Avg("engagement_score"))["avg"] or 0
            )
            characteristics["avg_engagement_score"] = avg_engagement

            # Add characteristics to result
            cluster_data["characteristics"] = characteristics

        return {
            "status": "success",
            "n_clusters": n_clusters,
            "clusters": clusters,
            "feature_names": [
                "gender",
                "age_group",
                "contact_method",
                "engagement",
                "contact_rate",
                "recent_activity",
            ],
        }

    @staticmethod
    def get_patient_cluster(patient_id, n_clusters=5):
        """Find which cluster a specific patient belongs to"""
        # Run clustering on all patients
        clustering_result = PatientClusteringService.cluster_patients(
            n_clusters=n_clusters
        )

        if clustering_result.get("status") != "success":
            return {
                "status": "error",
                "message": "Clustering failed",
                "details": clustering_result.get("message", "Unknown error"),
            }

        # Find which cluster contains this patient
        for cluster_name, cluster_data in clustering_result["clusters"].items():
            if patient_id in cluster_data["patient_ids"]:
                return {
                    "status": "success",
                    "cluster": cluster_name,
                    "characteristics": cluster_data["characteristics"],
                    "similar_patients_count": cluster_data["count"]
                    - 1,  # Excluding the patient themselves
                }

        return {
            "status": "not_found",
            "message": "Patient not included in clustering results",
        }
