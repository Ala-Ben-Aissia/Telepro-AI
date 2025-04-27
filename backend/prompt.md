# Telepro-AI: AI/ML Project Reference Prompt

## Purpose
This prompt serves as a shared reference for both developer and AI assistant to ensure all work, discussions, and code changes remain aligned with the project's real-world context, objectives, and best practices.

---

## Project Scope
- **Domain:** Patient engagement & campaign effectiveness in teleprospection.
- **Main Goal:** Build robust, interpretable, and production-ready AI/ML pipelines to predict patient responses and optimize campaign strategies.
- **Stakeholders:** Academic jury (FYP), company (internship), technical & non-technical users.

---

## Core AI/ML Requirements
- **Data Analysis:** In-depth EDA, outlier detection, correlation, and clustering for business insight.
- **Preprocessing:** Automated pipelines for cleaning, imputation, scaling, and encoding.
- **Feature Engineering:** Domain-driven features, interaction terms, and feature importance.
- **Segmentation:** Both rule-based and ML-driven (clustering, risk scoring) patient segmentation.
- **Modeling:** Ensemble models (RF, GB, stacking), robust hyperparameter tuning, and honest cross-validation.
- **Diagnostics:** Comprehensive, side-by-side visualizations (confusion matrix, ROC, PR curves) for training vs. cross-validation.
- **Evaluation:** Always report both optimistic (training) and realistic (CV/test) metrics.
- **Explainability:** Feature importance, clear documentation, and (future) SHAP/LIME.
- **Deployment:** Model persistence, API integration, and future support for real-time monitoring.

---

## Best Practices
- **Reproducibility:** Fixed random seeds, modular pipelines, versioned outputs, and experiment tracking.
- **Transparency:** All results and plots must be clearly labeled and explained for both technical and non-technical audiences.
- **Continuous Feedback:** Integrate user and stakeholder feedback into model and pipeline improvements.
- **Documentation:** Maintain up-to-date, professional documentation and code comments.

---

## Implementation Status (as of 2025-04-27)
- EDA, preprocessing, feature engineering, segmentation, ensemble modeling, SMOTE, cross-validation, and diagnostics: **Implemented**
- API integration for predictions: **Partially Implemented**
- Dynamic segmentation in campaigns, real-time monitoring, advanced explainability, external test set: **Not Yet Implemented**

---

## How to Use This Prompt
- Reference this file before making major changes or architectural decisions.
- Use it to align discussions, code reviews, and documentation.
- Update as the project evolves to keep all contributors on the same page.

---

_Last updated: 2025-04-27_
