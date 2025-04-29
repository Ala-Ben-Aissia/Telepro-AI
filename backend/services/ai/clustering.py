from sklearn.cluster import DBSCAN, KMeans
import numpy as np
from django.db.models import Avg, Count
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import io
import base64


class PatientClusteringService:
    """
    Service for clustering patients based on their features.
    Supports multiple clustering algorithms including K-means and DBSCAN.
    """

    @staticmethod
    def find_optimal_eps(features, n_samples=10):
        """
        Find optimal eps parameter for DBSCAN by analyzing the k-distance graph

        Args:
            features: Feature matrix
            n_samples: Number of samples to use for estimation

        Returns:
            float: Recommended eps value
        """
        # If dataset is large, sample it
        if len(features) > 1000:
            # Randomly select n_samples
            indices = np.random.choice(
                len(features), min(n_samples, len(features)), replace=False
            )
            sample_features = features[indices]
        else:
            sample_features = features

        # Calculate distances to nearest neighbors
        neighbors = NearestNeighbors(n_neighbors=5).fit(sample_features)
        distances, _ = neighbors.kneighbors(sample_features)

        # Sort distances to 5th nearest neighbor
        fifth_nn_distances = sorted(distances[:, 4])

        # Find "elbow" point in k-distance graph
        distance_diff = np.diff(fifth_nn_distances)

        # Find point where difference increases significantly
        threshold = np.mean(distance_diff) + np.std(distance_diff)
        elbow_idx = np.where(distance_diff > threshold)[0]

        if len(elbow_idx) > 0:
            # Take the first significant increase
            eps = fifth_nn_distances[elbow_idx[0]]
        else:
            # Fallback: take the value at 90th percentile
            eps = np.percentile(fifth_nn_distances, 90)

        # Create k-distance plot as base64 image
        plt.figure(figsize=(10, 6))
        plt.plot(fifth_nn_distances)
        plt.axhline(y=eps, color="r", linestyle="--")
        plt.ylabel("Distance to 5th nearest neighbor")
        plt.xlabel("Points (sorted)")
        plt.title("K-distance Graph for DBSCAN eps Selection")
        plt.grid(True)

        # Save plot to memory buffer
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close()

        # Convert to base64 for embedding in web
        plot_data = base64.b64encode(buf.read()).decode("utf-8")

        return eps, plot_data

    @staticmethod
    def cluster_with_dbscan(
        features, patient_ids, feature_names, eps=None, min_samples=5
    ):
        """
        Cluster patients using DBSCAN algorithm

        Args:
            features: Feature matrix
            patient_ids: List of patient IDs
            feature_names: List of feature names
            eps: DBSCAN eps parameter (distance threshold)
            min_samples: Minimum samples in neighborhood to form core point

        Returns:
            dict: Clustering results
        """
        from patients.models import Patient

        # Find optimal eps if not provided
        if eps is None:
            eps, k_distance_plot = PatientClusteringService.find_optimal_eps(features)
        else:
            k_distance_plot = None

        # Apply DBSCAN
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        cluster_labels = dbscan.fit_predict(features)

        # Get unique clusters (including -1 for noise)
        unique_clusters = np.unique(cluster_labels)

        # Prepare clusters dictionary
        clusters = {}
        for i in unique_clusters:
            cluster_name = f"Cluster_{i}" if i >= 0 else "Noise"
            cluster_indices = np.where(cluster_labels == i)[0]

            clusters[cluster_name] = {
                "patient_ids": [patient_ids[j] for j in cluster_indices],
                "count": len(cluster_indices),
                "is_noise": i == -1,
            }

            # Calculate centroid for non-noise clusters
            if i >= 0:
                # Get centroid by averaging features of cluster members
                cluster_features = features[cluster_indices]
                centroid = np.mean(cluster_features, axis=0)
                clusters[cluster_name]["centroid"] = centroid.tolist()

        # Add cluster characteristics (for non-noise clusters)
        for cluster_name, cluster_data in clusters.items():
            if cluster_data["is_noise"]:
                continue

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
            "algorithm": "DBSCAN",
            "parameters": {"eps": eps, "min_samples": min_samples},
            "n_clusters": len([c for c in unique_clusters if c >= 0]),  # Exclude noise
            "clusters": clusters,
            "feature_names": feature_names,
            "noise_count": sum(1 for label in cluster_labels if label == -1),
            "k_distance_plot": k_distance_plot,
        }

    @staticmethod
    def cluster_patients(
        algorithm="kmeans",
        n_clusters=5,
        include_only_with_consent=True,
        pipeline=None,
        eps=None,
        min_samples=5,
    ):
        """
        Cluster patients based on their features.

        Args:
            algorithm: Clustering algorithm ("kmeans" or "dbscan")
            n_clusters: Number of clusters (for KMeans)
            include_only_with_consent: Whether to only include patients with active consent
            pipeline: Optional preprocessing pipeline
            eps: DBSCAN distance threshold
            min_samples: DBSCAN min samples

        Returns:
            Dictionary with clustering results
        """
        from services.ai.preprocessing import DataPreprocessingService

        # Get preprocessed patient features
        if pipeline:
            features, patient_ids, used_pipeline, feature_names = (
                DataPreprocessingService.extract_patient_features(
                    include_only_with_consent=include_only_with_consent, pipeline=pipeline
                )
            )
        else:
            features, patient_ids, used_pipeline, feature_names = (
                DataPreprocessingService.extract_patient_features(
                    include_only_with_consent=include_only_with_consent
                )
            )

        if features is None or len(features) < 2:
            return {
                "status": "insufficient_data",
                "message": "Not enough patient data for clustering.",
            }

        # Choose clustering algorithm
        if algorithm.lower() == "dbscan":
            return PatientClusteringService.cluster_with_dbscan(
                features, patient_ids, feature_names, eps, min_samples
            )
        else:  # Default to KMeans
            # Make sure we have enough data for requested clusters
            if len(features) < n_clusters:
                return {
                    "status": "insufficient_data",
                    "message": f"Not enough patient data for {n_clusters} clusters.",
                }

            # Apply K-means clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(features)

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
            "algorithm": "KMeans",
            "n_clusters": n_clusters,
            "clusters": clusters,
            "feature_names": feature_names,
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
