import os
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from services.ai.preprocessing import DataPreprocessingService
from services.ai.clustering import PatientClusteringService

print("Telepro-AI AI Implementation Examples")
print("=====================================")

# Create output directory for generated files
output_dir = "example_outputs"
os.makedirs(output_dir, exist_ok=True)
print(f"Saving outputs to: {output_dir}")

# Create models directory
models_dir = os.path.join("models")
os.makedirs(models_dir, exist_ok=True)
print("\nImporting services...")
print("Services imported successfully")

# Example 1: Basic Feature Extraction
print("\n\nExample 1: Basic Feature Extraction")
print("-----------------------------------")
pipeline_path = os.path.join(output_dir, "patient_pipeline.joblib")
try:
    features, patient_ids, pipeline, feature_names = (
        DataPreprocessingService.extract_patient_features()
    )
    if features is None or len(features) == 0:
        print("No patient data available for feature extraction")
    else:
        print(f"Extracted features for {len(patient_ids)} patients")
        print(f"Feature matrix shape: {features.shape}")
        print(f"Number of features: {len(feature_names)}")
        print(f"First 5 feature names: {feature_names[:5]}")
        pipeline_path = os.path.join(output_dir, "patient_pipeline.joblib")
        DataPreprocessingService.save_pipeline(pipeline, filename=pipeline_path)
        print(f"Pipeline saved to {pipeline_path}")
except Exception as e:
    print(f"Error in Example 1: {str(e)}")
    features = None
    patient_ids = []
    pipeline = None
    feature_names = []

# Example 2: Feature DataFrame with Raw Data
print("\n\nExample 2: Feature DataFrame with Raw Data")
print("-----------------------------------------")
try:
    features_df, raw_df = DataPreprocessingService.extract_patient_features(
        return_dataframe=True, include_raw_data=True
    )
    print(f"Processed features DataFrame shape: {features_df.shape}")
    print(f"Raw data DataFrame shape: {raw_df.shape}")
    if not features_df.empty:
        print("\nProcessed features sample (first 3 columns):")
        print(features_df.iloc[:2, :3])
        print("\nRaw data sample (selected columns):")
        selected_cols = ["gender", "age_group", "engagement_score"]
        selected_cols = [col for col in selected_cols if col in raw_df.columns]
        print(raw_df[selected_cols].head(2))
        print("\nCreating feature distribution visualizations...")
        plt.figure(figsize=(12, 8))
        numeric_cols = features_df.select_dtypes(include=[np.number]).columns
        for i, col in enumerate(numeric_cols[:6]):
            plt.subplot(2, 3, i + 1)
            sns.histplot(features_df[col], kde=True)
            plt.title(col)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "feature_distributions.png"))
        print(f"Feature distributions saved to {output_dir}/feature_distributions.png")
    else:
        print("No data available for visualization")
except Exception as e:
    print(f"Error in Example 2: {str(e)}")

# Example 3: K-means Clustering
print("\n\nExample 3: K-means Clustering")
print("----------------------------")
kmeans_results = None
try:
    pipeline = DataPreprocessingService.load_pipeline(filename=pipeline_path)
    if pipeline:
        print("Successfully loaded preprocessing pipeline")
        kmeans_results = PatientClusteringService.cluster_patients(
            algorithm="kmeans",
            n_clusters=3,
            pipeline=pipeline,
        )
        print(f"Clustering status: {kmeans_results.get('status')}")
        if kmeans_results.get("status") == "success":
            print(f"Number of clusters: {kmeans_results.get('n_clusters')}")
            print("\nCluster sizes:")
            for cluster_name, cluster_data in kmeans_results.get("clusters", {}).items():
                print(f"  {cluster_name}: {cluster_data.get('count')} patients")
            first_cluster = next(iter(kmeans_results.get("clusters", {}).values()), {})
            if "characteristics" in first_cluster:
                print("\nSample cluster characteristics:")
                for key, value in first_cluster.get("characteristics", {}).items():
                    print(f"  {key}: {value}")
            import json

            filtered_results = {
                k: v for k, v in kmeans_results.items() if k != "pipeline"
            }

            def convert_for_json(obj):
                if isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, np.ndarray):
                    return obj.tolist()
                return obj

            with open(os.path.join(output_dir, "kmeans_results.json"), "w") as f:
                json.dump(filtered_results, f, default=convert_for_json, indent=2)
            print(f"K-means results saved to {output_dir}/kmeans_results.json")
    else:
        print("Failed to load pipeline")
except Exception as e:
    print(f"Error in Example 3: {str(e)}")

# Example 4: DBSCAN Clustering
print("\n\nExample 4: DBSCAN Clustering")
print("---------------------------")
try:
    if pipeline:
        dbscan_results = PatientClusteringService.cluster_patients(
            algorithm="dbscan", include_only_with_consent=True, pipeline=pipeline
        )
        print(f"DBSCAN status: {dbscan_results.get('status')}")
        if dbscan_results.get("status") == "success":
            print(f"Number of clusters found: {dbscan_results.get('n_clusters')}")
            print(f"Number of noise points: {dbscan_results.get('noise_count')}")
            print(
                f"EPS parameter used: {dbscan_results.get('parameters', {}).get('eps')}"
            )
            print("\nCluster sizes:")
            for cluster_name, cluster_data in dbscan_results.get("clusters", {}).items():
                print(f"  {cluster_name}: {cluster_data.get('count')} patients")
            k_distance_plot = dbscan_results.get("k_distance_plot")
            if k_distance_plot:
                import base64

                img_data = base64.b64decode(k_distance_plot)
                with open(os.path.join(output_dir, "k_distance_plot.png"), "wb") as f:
                    f.write(img_data)
                print(f"K-distance plot saved to {output_dir}/k_distance_plot.png")
    else:
        print("Pipeline not available for DBSCAN clustering")
except Exception as e:
    print(f"Error in Example 4: {str(e)}")

# Example 5: Get Aggregated Statistics
print("\n\nExample 5: Aggregated Statistics")
print("------------------------------")
try:
    stats = DataPreprocessingService.get_aggregated_statistics()
    print(f"Statistics status: {stats.get('status')}")
    if stats.get("status") == "success":
        print(f"Total patients: {stats.get('total_patients')}")
        demographics = stats.get("demographics", {})
        print("\nDemographics:")
        for category, distribution in demographics.items():
            print(f"  {category}:")
            for value, count in distribution.items():
                print(f"    {value}: {count}")
        engagement = stats.get("engagement", {})
        print("\nEngagement metrics:")
        for metric, value in engagement.items():
            print(f"  {metric}: {value:.2f}")
        channel_eff = stats.get("channel_effectiveness", {})
        print("\nChannel effectiveness:")
        for channel, metrics in channel_eff.items():
            print(f"  {channel}:")
            for metric, value in metrics.items():
                if value is not None:
                    if isinstance(value, (int, float)):
                        print(f"    {metric}: {value:.2f}")
                    else:
                        print(f"    {metric}: {value}")
        import json

        with open(os.path.join(output_dir, "patient_statistics.json"), "w") as f:
            json.dump(stats, f, indent=2)
        print(f"Statistics saved to {output_dir}/patient_statistics.json")
    else:
        print(f"Could not generate statistics: {stats.get('message')}")
except Exception as e:
    print(f"Error in Example 5: {str(e)}")

# Example 6: Feature Importance Analysis
print("\n\nExample 6: Feature Importance Analysis")
print("------------------------------------")
try:
    features, patient_ids, pipeline, feature_names = (
        DataPreprocessingService.extract_patient_features()
    )
    if features is not None and len(feature_names) > 0:
        importance_df = DataPreprocessingService.get_feature_importance(
            features, feature_names
        )
        print("Top 10 important features:")
        for i, (feature, importance) in enumerate(
            zip(importance_df["feature"], importance_df["importance"])
        ):
            print(f"  {i + 1}. {feature}: {importance:.4f}")
        plt.figure(figsize=(10, 6))
        sns.barplot(x="importance", y="feature", data=importance_df)
        plt.title("Feature Importance")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "feature_importance.png"))
        print(f"Feature importance plot saved to {output_dir}/feature_importance.png")
        importance_df.to_csv(
            os.path.join(output_dir, "feature_importance.csv"), index=False
        )
        print(f"Feature importance data saved to {output_dir}/feature_importance.csv")
    else:
        print("No features available for importance analysis")
except Exception as e:
    print(f"Error in Example 6: {str(e)}")

# Example 7: Compare Feature Distributions Across Clusters
print("\n\nExample 7: Compare Feature Distributions Across Clusters")
print("----------------------------------------------------")
try:
    features_df = DataPreprocessingService.extract_patient_features(
        return_dataframe=True, pipeline=pipeline
    )
    if not features_df.empty and kmeans_results and "clusters" in kmeans_results:
        clusters = kmeans_results["clusters"]
        cluster_mapping = {}
        for cluster_name, cluster_data in clusters.items():
            for patient_id in cluster_data["patient_ids"]:
                cluster_mapping[patient_id] = cluster_name
        features_df["cluster"] = features_df.index.map(
            lambda x: cluster_mapping.get(x, "Unknown")
        )
        numeric_features = features_df.select_dtypes(include=[np.number]).columns[:4]
        plt.figure(figsize=(15, 10))
        for i, feature in enumerate(numeric_features):
            plt.subplot(2, 2, i + 1)
            sns.boxplot(x="cluster", y=feature, data=features_df)
            plt.title(f"Distribution of {feature} by Cluster")
            plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "cluster_feature_comparison.png"))
        print(
            f"Cluster feature comparison saved to {output_dir}/cluster_feature_comparison.png"
        )
    else:
        print("Not enough data for cluster comparison")
except Exception as e:
    print(f"Error in Example 7: {str(e)}")

print("\n\nAll examples completed.")
print(f"Check the {output_dir} directory for output files.")
