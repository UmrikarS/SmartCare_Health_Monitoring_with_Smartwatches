"""
SmartCare Health Monitoring Project - Phase 2
Predictive Modeling and Clustering Analysis

Student: [Your Name]
Course: MBI806B
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import (mean_squared_error, r2_score, mean_absolute_error,
                             classification_report, confusion_matrix, accuracy_score,
                             roc_auc_score, roc_curve, silhouette_score)
import warnings

warnings.filterwarnings('ignore')

print("=" * 70)
print("SMARTCARE PREDICTIVE MODELING & CLUSTERING")
print("=" * 70)

# Load cleaned data
df = pd.read_csv('smartcare_cleaned_data.csv')
print(f"\n✓ Data loaded: {len(df)} records")

# ============================================================================
# 1. HEALTH SCORE PREDICTION MODEL
# ============================================================================

print("\n" + "=" * 70)
print("1. WEEKLY HEALTH SCORE PREDICTION MODEL")
print("=" * 70)

# Feature selection for health score prediction
feature_cols = ['Age', 'DailyStepCount', 'HeartRate_Avg', 'SleepDuration_Hours',
                'SleepQualityScore', 'StressIndex', 'CalorieBurn']
target_col = 'WeeklyHealthScore'

X = df[feature_cols].copy()
y = df[target_col].copy()

# Add gender as numeric
X['Gender_Male'] = (df['Gender'] == 'Male').astype(int)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

print(f"\nTraining set: {len(X_train)} samples")
print(f"Testing set: {len(X_test)} samples")

# Model 1: Multiple Linear Regression
print("\n--- Multiple Linear Regression ---")
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

y_pred_lr = lr_model.predict(X_test)
mse_lr = mean_squared_error(y_test, y_pred_lr)
rmse_lr = np.sqrt(mse_lr)
mae_lr = mean_absolute_error(y_test, y_pred_lr)
r2_lr = r2_score(y_test, y_pred_lr)

print(f"RMSE: {rmse_lr:.3f}")
print(f"MAE: {mae_lr:.3f}")
print(f"R² Score: {r2_lr:.3f}")

# Feature importance
feature_importance_lr = pd.DataFrame({
    'Feature': X.columns,
    'Coefficient': lr_model.coef_
}).sort_values('Coefficient', key=abs, ascending=False)

print("\nFeature Coefficients:")
for idx, row in feature_importance_lr.iterrows():
    print(f"  {row['Feature']}: {row['Coefficient']:.3f}")

# Model 2: Random Forest Regression
print("\n--- Random Forest Regression ---")
rf_model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
rf_model.fit(X_train, y_train)

y_pred_rf = rf_model.predict(X_test)
mse_rf = mean_squared_error(y_test, y_pred_rf)
rmse_rf = np.sqrt(mse_rf)
mae_rf = mean_absolute_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print(f"RMSE: {rmse_rf:.3f}")
print(f"MAE: {mae_rf:.3f}")
print(f"R² Score: {r2_rf:.3f}")

# Feature importance
feature_importance_rf = pd.DataFrame({
    'Feature': X.columns,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\nFeature Importance:")
for idx, row in feature_importance_rf.iterrows():
    print(f"  {row['Feature']}: {row['Importance']:.3f}")

# Cross-validation
cv_scores = cross_val_score(rf_model, X, y, cv=5, scoring='r2')
print(f"\nCross-Validation R² Scores: {cv_scores}")
print(f"Mean CV R²: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")

# Visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Health Score Prediction Models', fontsize=16, fontweight='bold')

# Plot 1: Linear Regression - Actual vs Predicted
axes[0, 0].scatter(y_test, y_pred_lr, alpha=0.6, color='blue')
axes[0, 0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()],
                'r--', linewidth=2, label='Perfect Prediction')
axes[0, 0].set_xlabel('Actual Health Score')
axes[0, 0].set_ylabel('Predicted Health Score')
axes[0, 0].set_title(f'Linear Regression (R² = {r2_lr:.3f})')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Plot 2: Random Forest - Actual vs Predicted
axes[0, 1].scatter(y_test, y_pred_rf, alpha=0.6, color='green')
axes[0, 1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()],
                'r--', linewidth=2, label='Perfect Prediction')
axes[0, 1].set_xlabel('Actual Health Score')
axes[0, 1].set_ylabel('Predicted Health Score')
axes[0, 1].set_title(f'Random Forest (R² = {r2_rf:.3f})')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# Plot 3: Feature Importance (RF)
top_features = feature_importance_rf.head(8)
axes[1, 0].barh(top_features['Feature'], top_features['Importance'], color='coral')
axes[1, 0].set_xlabel('Importance')
axes[1, 0].set_title('Top 8 Features (Random Forest)')
axes[1, 0].invert_yaxis()

# Plot 4: Residuals
residuals_rf = y_test - y_pred_rf
axes[1, 1].scatter(y_pred_rf, residuals_rf, alpha=0.6, color='purple')
axes[1, 1].axhline(y=0, color='r', linestyle='--', linewidth=2)
axes[1, 1].set_xlabel('Predicted Health Score')
axes[1, 1].set_ylabel('Residuals')
axes[1, 1].set_title('Residual Plot (Random Forest)')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('health_score_prediction.png', dpi=300, bbox_inches='tight')
print("\n✓ Health score prediction visualization saved")

# ============================================================================
# 2. FALL RISK PREDICTION MODEL
# ============================================================================

print("\n" + "=" * 70)
print("2. FALL RISK PREDICTION MODEL")
print("=" * 70)

# Feature selection for fall prediction
X_fall = df[['Age', 'DailyStepCount', 'SleepDuration_Hours', 'SleepQualityScore',
             'StressIndex', 'WeeklyHealthScore']].copy()
y_fall = df['FallAlerts'].copy()

print(f"\nClass Distribution:")
print(f"  No Falls: {(y_fall == 0).sum()} ({(y_fall == 0).sum() / len(y_fall) * 100:.1f}%)")
print(f"  Falls: {(y_fall == 1).sum()} ({(y_fall == 1).sum() / len(y_fall) * 100:.1f}%)")

# Train-test split
X_fall_train, X_fall_test, y_fall_train, y_fall_test = train_test_split(
    X_fall, y_fall, test_size=0.3, random_state=42, stratify=y_fall
)

# Logistic Regression
print("\n--- Logistic Regression ---")
log_model = LogisticRegression(random_state=42, max_iter=1000)
log_model.fit(X_fall_train, y_fall_train)

y_fall_pred_log = log_model.predict(X_fall_test)
y_fall_proba_log = log_model.predict_proba(X_fall_test)[:, 1]

accuracy_log = accuracy_score(y_fall_test, y_fall_pred_log)
print(f"Accuracy: {accuracy_log:.3f}")

if len(y_fall_test.unique()) > 1:
    auc_log = roc_auc_score(y_fall_test, y_fall_proba_log)
    print(f"AUC-ROC: {auc_log:.3f}")

print("\nClassification Report:")
print(classification_report(y_fall_test, y_fall_pred_log, target_names=['No Fall', 'Fall']))

# Feature coefficients
fall_features = pd.DataFrame({
    'Feature': X_fall.columns,
    'Coefficient': log_model.coef_[0]
}).sort_values('Coefficient', key=abs, ascending=False)

print("\nFeature Coefficients (Fall Risk Factors):")
for idx, row in fall_features.iterrows():
    direction = "↑ increases" if row['Coefficient'] > 0 else "↓ decreases"
    print(f"  {row['Feature']}: {row['Coefficient']:.3f} ({direction} fall risk)")

# Random Forest Classifier
print("\n--- Random Forest Classifier ---")
rf_fall_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
rf_fall_model.fit(X_fall_train, y_fall_train)

y_fall_pred_rf = rf_fall_model.predict(X_fall_test)
y_fall_proba_rf = rf_fall_model.predict_proba(X_fall_test)[:, 1]

accuracy_rf_fall = accuracy_score(y_fall_test, y_fall_pred_rf)
print(f"Accuracy: {accuracy_rf_fall:.3f}")

if len(y_fall_test.unique()) > 1:
    auc_rf_fall = roc_auc_score(y_fall_test, y_fall_proba_rf)
    print(f"AUC-ROC: {auc_rf_fall:.3f}")

print("\nClassification Report:")
print(classification_report(y_fall_test, y_fall_pred_rf, target_names=['No Fall', 'Fall']))

# Visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Fall Risk Prediction Models', fontsize=16, fontweight='bold')

# Plot 1: Confusion Matrix - Logistic Regression
cm_log = confusion_matrix(y_fall_test, y_fall_pred_log)
sns.heatmap(cm_log, annot=True, fmt='d', cmap='Blues', ax=axes[0, 0],
            xticklabels=['No Fall', 'Fall'], yticklabels=['No Fall', 'Fall'])
axes[0, 0].set_title('Confusion Matrix - Logistic Regression')
axes[0, 0].set_ylabel('Actual')
axes[0, 0].set_xlabel('Predicted')

# Plot 2: Confusion Matrix - Random Forest
cm_rf = confusion_matrix(y_fall_test, y_fall_pred_rf)
sns.heatmap(cm_rf, annot=True, fmt='d', cmap='Greens', ax=axes[0, 1],
            xticklabels=['No Fall', 'Fall'], yticklabels=['No Fall', 'Fall'])
axes[0, 1].set_title('Confusion Matrix - Random Forest')
axes[0, 1].set_ylabel('Actual')
axes[0, 1].set_xlabel('Predicted')

# Plot 3: ROC Curves
if len(y_fall_test.unique()) > 1:
    fpr_log, tpr_log, _ = roc_curve(y_fall_test, y_fall_proba_log)
    fpr_rf, tpr_rf, _ = roc_curve(y_fall_test, y_fall_proba_rf)

    axes[1, 0].plot(fpr_log, tpr_log, label=f'Logistic Reg (AUC={auc_log:.3f})', linewidth=2)
    axes[1, 0].plot(fpr_rf, tpr_rf, label=f'Random Forest (AUC={auc_rf_fall:.3f})', linewidth=2)
    axes[1, 0].plot([0, 1], [0, 1], 'k--', label='Random Classifier')
    axes[1, 0].set_xlabel('False Positive Rate')
    axes[1, 0].set_ylabel('True Positive Rate')
    axes[1, 0].set_title('ROC Curves')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

# Plot 4: Feature Importance (RF)
fall_importance = pd.DataFrame({
    'Feature': X_fall.columns,
    'Importance': rf_fall_model.feature_importances_
}).sort_values('Importance', ascending=False)

axes[1, 1].barh(fall_importance['Feature'], fall_importance['Importance'], color='crimson')
axes[1, 1].set_xlabel('Importance')
axes[1, 1].set_title('Feature Importance - Fall Risk')
axes[1, 1].invert_yaxis()

plt.tight_layout()
plt.savefig('fall_risk_prediction.png', dpi=300, bbox_inches='tight')
print("\n✓ Fall risk prediction visualization saved")

# ============================================================================
# 3. K-MEANS CLUSTERING FOR PATIENT SEGMENTATION
# ============================================================================

print("\n" + "=" * 70)
print("3. K-MEANS CLUSTERING - PATIENT SEGMENTATION")
print("=" * 70)

# Select features for clustering
cluster_features = ['Age', 'DailyStepCount', 'SleepDuration_Hours',
                    'StressIndex', 'WeeklyHealthScore']
X_cluster = df[cluster_features].copy()

# Standardize features
scaler = StandardScaler()
X_cluster_scaled = scaler.fit_transform(X_cluster)

# Determine optimal number of clusters using Elbow Method
print("\n--- Elbow Method for Optimal K ---")
inertias = []
silhouette_scores = []
K_range = range(2, 8)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_cluster_scaled)
    inertias.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(X_cluster_scaled, kmeans.labels_))
    print(f"K={k}: Inertia={kmeans.inertia_:.2f}, Silhouette Score={silhouette_scores[-1]:.3f}")

# Choose optimal K (based on elbow and silhouette)
optimal_k = 4
print(f"\n✓ Selected K = {optimal_k} clusters")

# Fit final model
kmeans_final = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
df['Cluster'] = kmeans_final.fit_predict(X_cluster_scaled)

print(f"\nCluster Distribution:")
cluster_dist = df['Cluster'].value_counts().sort_index()
for cluster_id in cluster_dist.index:
    count = cluster_dist[cluster_id]
    pct = (count / len(df)) * 100
    print(f"  Cluster {cluster_id}: {count} patients ({pct:.1f}%)")

# Cluster profiles
print("\n--- Cluster Profiles ---")
cluster_profiles = df.groupby('Cluster')[cluster_features + ['Risk_Score', 'FallAlerts']].mean()
print(cluster_profiles.round(2))

# Interpret clusters
print("\nCluster Interpretation:")
for i in range(optimal_k):
    profile = cluster_profiles.loc[i]
    print(f"\nCluster {i}:")
    print(f"  Average Age: {profile['Age']:.1f} years")
    print(f"  Activity: {profile['DailyStepCount']:.0f} steps/day")
    print(f"  Sleep: {profile['SleepDuration_Hours']:.1f} hours/day")
    print(f"  Stress: {profile['StressIndex']:.1f}/100")
    print(f"  Health Score: {profile['WeeklyHealthScore']:.1f}/100")
    print(f"  Risk Score: {profile['Risk_Score']:.1f}/100")
    print(f"  Fall Rate: {profile['FallAlerts']:.2%}")

    # Label cluster
    if profile['WeeklyHealthScore'] >= 85 and profile['Risk_Score'] < 40:
        label = "Healthy & Active"
    elif profile['Risk_Score'] >= 60:
        label = "High Risk - Needs Intervention"
    elif profile['StressIndex'] >= 70:
        label = "Moderate Risk - Stress Management"
    else:
        label = "Moderate Risk - General Monitoring"

    print(f"  Label: {label}")
    df.loc[df['Cluster'] == i, 'Cluster_Label'] = label

# Visualization
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('K-Means Clustering Analysis', fontsize=16, fontweight='bold')

# Plot 1: Elbow curve
axes[0, 0].plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
axes[0, 0].set_xlabel('Number of Clusters (K)')
axes[0, 0].set_ylabel('Inertia')
axes[0, 0].set_title('Elbow Method')
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].axvline(optimal_k, color='red', linestyle='--', label=f'Optimal K={optimal_k}')
axes[0, 0].legend()

# Plot 2: Silhouette scores
axes[0, 1].plot(K_range, silhouette_scores, 'go-', linewidth=2, markersize=8)
axes[0, 1].set_xlabel('Number of Clusters (K)')
axes[0, 1].set_ylabel('Silhouette Score')
axes[0, 1].set_title('Silhouette Analysis')
axes[0, 1].grid(True, alpha=0.3)
axes[0, 1].axvline(optimal_k, color='red', linestyle='--', label=f'Optimal K={optimal_k}')
axes[0, 1].legend()

# Plot 3: Cluster distribution
cluster_counts = df['Cluster'].value_counts().sort_index()
axes[0, 2].bar(cluster_counts.index, cluster_counts.values, color='skyblue', edgecolor='black')
axes[0, 2].set_xlabel('Cluster')
axes[0, 2].set_ylabel('Patient Count')
axes[0, 2].set_title('Cluster Distribution')
for i, v in enumerate(cluster_counts.values):
    axes[0, 2].text(i, v + 0.5, str(v), ha='center', fontweight='bold')

# Plot 4: Age vs Health Score by Cluster
scatter = axes[1, 0].scatter(df['Age'], df['WeeklyHealthScore'],
                             c=df['Cluster'], cmap='viridis', alpha=0.6, s=50)
axes[1, 0].set_xlabel('Age')
axes[1, 0].set_ylabel('Weekly Health Score')
axes[1, 0].set_title('Clusters: Age vs Health Score')
plt.colorbar(scatter, ax=axes[1, 0], label='Cluster')
axes[1, 0].grid(True, alpha=0.3)

# Plot 5: Steps vs Stress by Cluster
scatter2 = axes[1, 1].scatter(df['DailyStepCount'], df['StressIndex'],
                              c=df['Cluster'], cmap='viridis', alpha=0.6, s=50)
axes[1, 1].set_xlabel('Daily Step Count')
axes[1, 1].set_ylabel('Stress Index')
axes[1, 1].set_title('Clusters: Activity vs Stress')
plt.colorbar(scatter2, ax=axes[1, 1], label='Cluster')
axes[1, 1].grid(True, alpha=0.3)

# Plot 6: Cluster profiles heatmap
profile_data = cluster_profiles[cluster_features].T
sns.heatmap(profile_data, annot=True, fmt='.1f', cmap='YlGnBu', ax=axes[1, 2])
axes[1, 2].set_title('Cluster Profiles Heatmap')
axes[1, 2].set_xlabel('Cluster')
axes[1, 2].set_ylabel('Feature')

plt.tight_layout()
plt.savefig('clustering_analysis.png', dpi=300, bbox_inches='tight')
print("\n✓ Clustering visualization saved")

# ============================================================================
# 4. RISK SCORE VALIDATION
# ============================================================================

print("\n" + "=" * 70)
print("4. RISK SCORE VALIDATION")
print("=" * 70)

# Compare risk score with actual health outcomes
risk_categories = ['Low Risk', 'Medium Risk', 'High Risk', 'Critical Risk']

print("\nHealth Outcomes by Risk Category:")
for category in risk_categories:
    if category in df['RiskCategory'].values:
        subset = df[df['RiskCategory'] == category]
        print(f"\n{category} (n={len(subset)}):")
        print(f"  Avg Health Score: {subset['WeeklyHealthScore'].mean():.1f}")
        print(f"  Avg Age: {subset['Age'].mean():.1f}")
        print(f"  Fall Rate: {(subset['FallAlerts'].sum() / len(subset) * 100):.1f}%")
        print(
            f"  High Stress (>70): {(subset['StressIndex'] > 70).sum()} ({(subset['StressIndex'] > 70).sum() / len(subset) * 100:.1f}%)")
        print(
            f"  Poor Sleep (<6h): {(subset['SleepDuration_Hours'] < 6).sum()} ({(subset['SleepDuration_Hours'] < 6).sum() / len(subset) * 100:.1f}%)")

# Correlation between risk score and outcomes
print("\nRisk Score Correlations:")
print(f"  Risk Score vs Health Score: r = {df['Risk_Score'].corr(df['WeeklyHealthScore']):.3f}")
print(f"  Risk Score vs Stress Index: r = {df['Risk_Score'].corr(df['StressIndex']):.3f}")
print(f"  Risk Score vs Age: r = {df['Risk_Score'].corr(df['Age']):.3f}")

# ============================================================================
# 5. SAVE ENHANCED DATASET
# ============================================================================

print("\n" + "=" * 70)
print("5. SAVE ENHANCED DATASET")
print("=" * 70)

# Save dataset with predictions and clusters
df.to_csv('smartcare_with_predictions.csv', index=False)
print("\n✓ Enhanced dataset saved: 'smartcare_with_predictions.csv'")
print(f"  Added columns: Cluster, Cluster_Label")

# ============================================================================
# 6. MODEL PERFORMANCE SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("MODEL PERFORMANCE SUMMARY")
print("=" * 70)

summary_data = {
    'Model': [
        'Linear Regression (Health Score)',
        'Random Forest (Health Score)',
        'Logistic Regression (Fall Risk)',
        'Random Forest (Fall Risk)',
        'K-Means Clustering'
    ],
    'Primary Metric': [
        f'R² = {r2_lr:.3f}',
        f'R² = {r2_rf:.3f}',
        f'Accuracy = {accuracy_log:.3f}',
        f'Accuracy = {accuracy_rf_fall:.3f}',
        f'Silhouette = {silhouette_scores[optimal_k - 2]:.3f}'
    ],
    'Performance': [
        'Good' if r2_lr > 0.6 else 'Moderate',
        'Excellent' if r2_rf > 0.7 else 'Good',
        'Good' if accuracy_log > 0.75 else 'Moderate',
        'Good' if accuracy_rf_fall > 0.75 else 'Moderate',
        'Good' if silhouette_scores[optimal_k - 2] > 0.4 else 'Moderate'
    ]
}

summary_df = pd.DataFrame(summary_data)
print("\n" + summary_df.to_string(index=False))

print("\n" + "=" * 70)
print("KEY PREDICTIVE INSIGHTS")
print("=" * 70)

print("\n1. HEALTH SCORE PREDICTION:")
print(f"   • Best model: Random Forest (R² = {r2_rf:.3f})")
print(f"   • Top 3 predictors: {', '.join(feature_importance_rf.head(3)['Feature'].tolist())}")
print(f"   • Model can explain {r2_rf * 100:.1f}% of health score variation")

print("\n2. FALL RISK PREDICTION:")
print(f"   • Model accuracy: {accuracy_rf_fall * 100:.1f}%")
print(f"   • Key risk factors: {', '.join(fall_importance.head(3)['Feature'].tolist())}")
if len(y_fall_test.unique()) > 1:
    print(f"   • AUC-ROC: {auc_rf_fall:.3f}")

print("\n3. PATIENT SEGMENTATION:")
print(f"   • Optimal clusters: {optimal_k}")
print(f"   • Silhouette score: {silhouette_scores[optimal_k - 2]:.3f}")
print("   • Clusters enable targeted intervention strategies")

print("\n" + "=" * 70)
print("PREDICTIVE MODELING COMPLETE")
print("=" * 70)
print("\nGenerated Outputs:")
print("  1. health_score_prediction.png")
print("  2. fall_risk_prediction.png")
print("  3. clustering_analysis.png")
print("  4. smartcare_with_predictions.csv")
print("\nNext Steps:")
print("  • Create Power BI dashboard")
print("  • Develop intervention recommendations")
print("  • Document methodology in report")
print("=" * 70)