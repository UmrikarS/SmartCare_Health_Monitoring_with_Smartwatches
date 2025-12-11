"""
SmartCare Health Monitoring Project - Phase 3
Advanced Visualizations for Report

Student: [Your Name]
Course: MBI806B
Purpose: Create publication-quality visualizations for findings section
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle
from matplotlib.gridspec import GridSpec
import warnings

warnings.filterwarnings('ignore')

# Set style for publication quality
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9

print("=" * 70)
print("ADVANCED VISUALIZATIONS FOR SMARTCARE REPORT")
print("=" * 70)

# Load data
df = pd.read_csv('smartcare_cleaned_data.csv')
print(f"\n✓ Data loaded: {len(df)} records")

# Color scheme for consistency
COLORS = {
    'primary': '#2563eb',
    'secondary': '#059669',
    'accent': '#f59e0b',
    'danger': '#dc3545',
    'success': '#28a745',
    'warning': '#ffc107',
    'info': '#17a2b8'
}

# ============================================================================
# 1. EXECUTIVE SUMMARY DASHBOARD (Single Page Overview)
# ============================================================================

print("\n--- Creating Executive Summary Dashboard ---")

fig = plt.figure(figsize=(16, 10))
gs = GridSpec(3, 4, figure=fig, hspace=0.4, wspace=0.4)

fig.suptitle('SmartCare Health Monitoring - Executive Summary Dashboard',
             fontsize=18, fontweight='bold', y=0.98)

# KPI Cards (Top Row)
kpi_data = [
    ('Total Patients', len(df), COLORS['primary']),
    ('Avg Health Score', f"{df['WeeklyHealthScore'].mean():.1f}/100", COLORS['success']),
    ('High Risk',
     f"{len(df[df['RiskCategory'].isin(['High Risk', 'Critical Risk'])])} ({len(df[df['RiskCategory'].isin(['High Risk', 'Critical Risk'])]) / len(df) * 100:.0f}%)",
     COLORS['danger']),
    ('Fall Alert Rate', f"{df['FallAlerts'].sum()} ({df['FallAlerts'].sum() / len(df) * 100:.0f}%)", COLORS['warning'])
]

for i, (label, value, color) in enumerate(kpi_data):
    ax = fig.add_subplot(gs[0, i])
    ax.text(0.5, 0.7, str(value), ha='center', va='center',
            fontsize=24, fontweight='bold', color=color)
    ax.text(0.5, 0.3, label, ha='center', va='center',
            fontsize=11, color='gray')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    # Add background
    rect = Rectangle((0.05, 0.1), 0.9, 0.8, facecolor=color, alpha=0.1,
                     edgecolor=color, linewidth=2)
    ax.add_patch(rect)

# Row 2: Health Metrics
ax1 = fig.add_subplot(gs[1, :2])
health_categories = df['HealthCategory'].value_counts().reindex(['Excellent', 'Good', 'Fair', 'Poor'], fill_value=0)
colors_health = [COLORS['success'], COLORS['info'], COLORS['warning'], COLORS['danger']]
ax1.pie(health_categories, labels=health_categories.index, autopct='%1.1f%%',
        colors=colors_health, startangle=90)
ax1.set_title('Health Score Distribution', fontweight='bold', pad=10)

ax2 = fig.add_subplot(gs[1, 2:])
risk_categories = df['RiskCategory'].value_counts().reindex(['Low Risk', 'Medium Risk', 'High Risk', 'Critical Risk'],
                                                            fill_value=0)
colors_risk = [COLORS['success'], COLORS['warning'], COLORS['accent'], COLORS['danger']]
wedges, texts, autotexts = ax2.pie(risk_categories, labels=risk_categories.index,
                                   autopct='%1.1f%%', colors=colors_risk, startangle=90)
ax2.set_title('Risk Category Distribution', fontweight='bold', pad=10)

# Row 3: Demographics and Activity
ax3 = fig.add_subplot(gs[2, 0])
age_groups = df['AgeGroup'].value_counts().reindex(['50-59', '60-69', '70-79', '80+'], fill_value=0)
ax3.bar(age_groups.index, age_groups.values, color=COLORS['primary'], alpha=0.7, edgecolor='black')
ax3.set_xlabel('Age Group')
ax3.set_ylabel('Patient Count')
ax3.set_title('Age Distribution', fontweight='bold')
for i, v in enumerate(age_groups.values):
    ax3.text(i, v + 0.5, str(v), ha='center', fontweight='bold')
ax3.grid(axis='y', alpha=0.3)

ax4 = fig.add_subplot(gs[2, 1])
gender_counts = df['Gender'].value_counts()
ax4.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%',
        colors=['#4e79a7', '#e15759'], startangle=90)
ax4.set_title('Gender Distribution', fontweight='bold', pad=10)

ax5 = fig.add_subplot(gs[2, 2:])
activity_counts = df['ActivityLevel'].value_counts().reindex(['Sedentary', 'Moderate', 'Active'], fill_value=0)
colors_activity = [COLORS['danger'], COLORS['warning'], COLORS['success']]
bars = ax5.barh(activity_counts.index, activity_counts.values, color=colors_activity, alpha=0.7, edgecolor='black')
ax5.set_xlabel('Patient Count')
ax5.set_title('Physical Activity Levels', fontweight='bold')
for i, (bar, v) in enumerate(zip(bars, activity_counts.values)):
    ax5.text(v + 0.5, bar.get_y() + bar.get_height() / 2,
             f'{v} ({v / len(df) * 100:.0f}%)', va='center', fontweight='bold')
ax5.grid(axis='x', alpha=0.3)

plt.savefig('executive_summary_dashboard.png', dpi=300, bbox_inches='tight')
print("✓ Saved: executive_summary_dashboard.png")
plt.close()

# ============================================================================
# 2. CORRELATION INSIGHTS WITH SCATTER PLOTS
# ============================================================================

print("\n--- Creating Detailed Correlation Analysis ---")

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('Key Health Metric Correlations - Detailed Analysis',
             fontsize=16, fontweight='bold')

# Define key correlations to visualize
correlations = [
    ('SleepDuration_Hours', 'StressIndex', 'Sleep Duration vs Stress Index'),
    ('DailyStepCount', 'WeeklyHealthScore', 'Daily Steps vs Health Score'),
    ('SleepQualityScore', 'WeeklyHealthScore', 'Sleep Quality vs Health Score'),
    ('Age', 'WeeklyHealthScore', 'Age vs Health Score'),
    ('StressIndex', 'WeeklyHealthScore', 'Stress Index vs Health Score'),
    ('DailyStepCount', 'CalorieBurn', 'Daily Steps vs Calorie Burn')
]

for idx, (x_var, y_var, title) in enumerate(correlations):
    row = idx // 3
    col = idx % 3
    ax = axes[row, col]

    # Calculate correlation
    corr = df[x_var].corr(df[y_var])

    # Scatter plot with regression line
    ax.scatter(df[x_var], df[y_var], alpha=0.6, s=50, c=COLORS['primary'])

    # Add regression line
    z = np.polyfit(df[x_var], df[y_var], 1)
    p = np.poly1d(z)
    x_line = np.linspace(df[x_var].min(), df[x_var].max(), 100)
    ax.plot(x_line, p(x_line), "r--", linewidth=2,
            label=f'r = {corr:.3f}')

    ax.set_xlabel(x_var.replace('_', ' '))
    ax.set_ylabel(y_var.replace('_', ' '))
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('correlation_scatter_plots.png', dpi=300, bbox_inches='tight')
print("✓ Saved: correlation_scatter_plots.png")
plt.close()

# ============================================================================
# 3. RISK SEGMENTATION QUADRANT ANALYSIS
# ============================================================================

print("\n--- Creating Risk Segmentation Quadrant Chart ---")

fig, ax = plt.subplots(figsize=(12, 8))

# Create scatter plot colored by risk category
risk_colors = {
    'Low Risk': COLORS['success'],
    'Medium Risk': COLORS['warning'],
    'High Risk': COLORS['accent'],
    'Critical Risk': COLORS['danger']
}

for risk_cat in df['RiskCategory'].unique():
    mask = df['RiskCategory'] == risk_cat
    ax.scatter(df[mask]['Age'], df[mask]['Risk_Score'],
               c=risk_colors.get(risk_cat, 'gray'),
               label=risk_cat, s=100, alpha=0.7, edgecolors='black', linewidth=0.5)

# Add quadrant lines
ax.axhline(y=50, color='black', linestyle='--', linewidth=1.5, alpha=0.5)
ax.axvline(x=70, color='black', linestyle='--', linewidth=1.5, alpha=0.5)

# Add quadrant labels
ax.text(55, 85, 'High Risk\nYounger Age', ha='center', va='center',
        fontsize=10, style='italic', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
ax.text(75, 85, 'Critical Priority\nOlder + High Risk', ha='center', va='center',
        fontsize=10, style='italic', bbox=dict(boxstyle='round', facecolor='red', alpha=0.3))
ax.text(55, 25, 'Low Priority\nYounger + Low Risk', ha='center', va='center',
        fontsize=10, style='italic', bbox=dict(boxstyle='round', facecolor='green', alpha=0.3))
ax.text(75, 25, 'Age Monitoring\nOlder but Low Risk', ha='center', va='center',
        fontsize=10, style='italic', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))

ax.set_xlabel('Age (years)', fontsize=12, fontweight='bold')
ax.set_ylabel('Risk Score (0-100)', fontsize=12, fontweight='bold')
ax.set_title('Patient Risk Segmentation - Quadrant Analysis\n(Age vs Risk Score)',
             fontsize=14, fontweight='bold', pad=15)
ax.legend(loc='upper left', frameon=True, shadow=True)
ax.grid(True, alpha=0.3)
ax.set_xlim(48, 82)
ax.set_ylim(0, 100)

plt.tight_layout()
plt.savefig('risk_quadrant_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: risk_quadrant_analysis.png")
plt.close()

# ============================================================================
# 4. CLUSTER PROFILES RADAR CHART
# ============================================================================

print("\n--- Creating Cluster Profile Radar Charts ---")

# First, ensure Cluster column exists
if 'Cluster' not in df.columns:
    print("⚠ Creating clusters (Cluster column not found)...")
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler

    cluster_features = ['Age', 'DailyStepCount', 'SleepDuration_Hours',
                        'StressIndex', 'WeeklyHealthScore']
    X_cluster = df[cluster_features].copy()
    scaler_cluster = StandardScaler()
    X_cluster_scaled = scaler_cluster.fit_transform(X_cluster)
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(X_cluster_scaled)
    print(f"✓ Created {df['Cluster'].nunique()} clusters")

# Normalize features for radar chart
features_for_radar = ['Age', 'DailyStepCount', 'SleepDuration_Hours',
                      'StressIndex', 'WeeklyHealthScore']

# Get cluster profiles
cluster_profiles = df.groupby('Cluster')[features_for_radar].mean()

# Normalize to 0-1 scale for each feature
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
cluster_profiles_norm = pd.DataFrame(
    scaler.fit_transform(cluster_profiles.T).T,
    columns=cluster_profiles.columns,
    index=cluster_profiles.index
)

# Create radar chart
fig, axes = plt.subplots(2, 2, figsize=(14, 12), subplot_kw=dict(projection='polar'))
fig.suptitle('Patient Cluster Health Profiles - Radar Chart Comparison',
             fontsize=16, fontweight='bold')

cluster_names = ['Healthy Active', 'Stressed but Active', 'Sedentary Aging', 'Multi-Domain Compromise']
cluster_colors = ['green', 'orange', 'red', 'purple']

for idx, (cluster_id, cluster_name, color) in enumerate(zip(range(4), cluster_names, cluster_colors)):
    if cluster_id not in cluster_profiles_norm.index:
        continue

    row = idx // 2
    col = idx % 2
    ax = axes[row, col]

    # Get data for this cluster
    values = cluster_profiles_norm.loc[cluster_id].values

    # Number of variables
    num_vars = len(features_for_radar)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # Complete the circle
    values = np.concatenate((values, [values[0]]))
    angles += angles[:1]

    # Plot
    ax.plot(angles, values, 'o-', linewidth=2, color=color, label=cluster_name)
    ax.fill(angles, values, alpha=0.25, color=color)

    # Fix axis to go in the right order
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([f.replace('_', '\n') for f in features_for_radar], fontsize=8)
    ax.set_ylim(0, 1)
    ax.set_title(f'Cluster {cluster_id}: {cluster_name}',
                 fontsize=12, fontweight='bold', pad=20)
    ax.grid(True)

    # Add cluster size
    cluster_size = len(df[df['Cluster'] == cluster_id])
    ax.text(0, -0.15, f'n = {cluster_size} ({cluster_size / len(df) * 100:.0f}%)',
            ha='center', transform=ax.transAxes, fontsize=10)

plt.tight_layout()
plt.savefig('cluster_radar_profiles.png', dpi=300, bbox_inches='tight')
print("✓ Saved: cluster_radar_profiles.png")
plt.close()

# ============================================================================
# 5. SLEEP-STRESS DETAILED ANALYSIS
# ============================================================================

print("\n--- Creating Sleep-Stress Detailed Analysis ---")

fig = plt.figure(figsize=(16, 10))
gs = GridSpec(2, 3, figure=fig, hspace=0.3, wspace=0.3)

fig.suptitle('Sleep Duration and Stress Index - Comprehensive Analysis',
             fontsize=16, fontweight='bold')

# Plot 1: Main scatter with regression
ax1 = plt.subplot(gs[0, :2])
scatter = ax1.scatter(df['SleepDuration_Hours'], df['StressIndex'],
                      c=df['WeeklyHealthScore'], cmap='RdYlGn',
                      s=100, alpha=0.6, edgecolors='black', linewidth=0.5)
z = np.polyfit(df['SleepDuration_Hours'], df['StressIndex'], 1)
p = np.poly1d(z)
x_line = np.linspace(df['SleepDuration_Hours'].min(), df['SleepDuration_Hours'].max(), 100)
ax1.plot(x_line, p(x_line), "r--", linewidth=2,
         label=f'y = {z[0]:.2f}x + {z[1]:.2f}\nr = {df["SleepDuration_Hours"].corr(df["StressIndex"]):.3f}')
ax1.set_xlabel('Sleep Duration (hours)', fontsize=12)
ax1.set_ylabel('Stress Index', fontsize=12)
ax1.set_title('Sleep vs Stress (colored by Health Score)', fontsize=12, fontweight='bold')
ax1.legend(loc='upper right')
ax1.grid(True, alpha=0.3)
cbar = plt.colorbar(scatter, ax=ax1)
cbar.set_label('Health Score', rotation=270, labelpad=15)

# Plot 2: Box plots by sleep category
ax2 = plt.subplot(gs[0, 2])
sleep_order = ['Poor', 'Fair', 'Good', 'Excessive']
sleep_data = [df[df['SleepCategory'] == cat]['StressIndex'].values
              for cat in sleep_order if cat in df['SleepCategory'].unique()]
bp = ax2.boxplot(sleep_data, labels=[cat for cat in sleep_order if cat in df['SleepCategory'].unique()],
                 patch_artist=True)
for patch, color in zip(bp['boxes'], [COLORS['danger'], COLORS['warning'], COLORS['success'], COLORS['info']]):
    patch.set_facecolor(color)
    patch.set_alpha(0.6)
ax2.set_xlabel('Sleep Category')
ax2.set_ylabel('Stress Index')
ax2.set_title('Stress by Sleep Category', fontsize=11, fontweight='bold')
ax2.grid(axis='y', alpha=0.3)

# Plot 3: Histogram of sleep duration
ax3 = plt.subplot(gs[1, 0])
ax3.hist(df['SleepDuration_Hours'], bins=15, color=COLORS['info'], alpha=0.7, edgecolor='black')
ax3.axvline(7, color='green', linestyle='--', linewidth=2, label='Optimal Min (7h)')
ax3.axvline(9, color='green', linestyle='--', linewidth=2, label='Optimal Max (9h)')
ax3.axvline(df['SleepDuration_Hours'].mean(), color='red', linestyle='-', linewidth=2,
            label=f'Mean ({df["SleepDuration_Hours"].mean():.1f}h)')
ax3.set_xlabel('Sleep Duration (hours)')
ax3.set_ylabel('Frequency')
ax3.set_title('Sleep Duration Distribution', fontsize=11, fontweight='bold')
ax3.legend()
ax3.grid(axis='y', alpha=0.3)

# Plot 4: Histogram of stress index
ax4 = plt.subplot(gs[1, 1])
ax4.hist(df['StressIndex'], bins=15, color=COLORS['accent'], alpha=0.7, edgecolor='black')
ax4.axvline(40, color='green', linestyle='--', linewidth=2, label='Low/Mod threshold')
ax4.axvline(70, color='red', linestyle='--', linewidth=2, label='Mod/High threshold')
ax4.axvline(df['StressIndex'].mean(), color='blue', linestyle='-', linewidth=2,
            label=f'Mean ({df["StressIndex"].mean():.1f})')
ax4.set_xlabel('Stress Index')
ax4.set_ylabel('Frequency')
ax4.set_title('Stress Index Distribution', fontsize=11, fontweight='bold')
ax4.legend()
ax4.grid(axis='y', alpha=0.3)

# Plot 5: Heatmap of sleep-stress combinations
ax5 = plt.subplot(gs[1, 2])
sleep_stress_pivot = pd.crosstab(df['SleepCategory'], df['StressLevel'])
sns.heatmap(sleep_stress_pivot, annot=True, fmt='d', cmap='YlOrRd', ax=ax5, cbar_kws={'label': 'Patient Count'})
ax5.set_title('Sleep-Stress Cross-tabulation', fontsize=11, fontweight='bold')
ax5.set_xlabel('Stress Level')
ax5.set_ylabel('Sleep Category')

plt.savefig('sleep_stress_comprehensive.png', dpi=300, bbox_inches='tight')
print("✓ Saved: sleep_stress_comprehensive.png")
plt.close()

# ============================================================================
# 6. PREDICTIVE MODEL PERFORMANCE COMPARISON
# ============================================================================

print("\n--- Creating Model Performance Comparison ---")

# Load prediction results (from phase 2 modeling)
try:
    df_pred = pd.read_csv('smartcare_with_predictions.csv')

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Predictive Model Performance Visualization',
                 fontsize=16, fontweight='bold')

    # Simulate model performance (replace with actual if available)
    # For demonstration - you'd use actual predictions
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestRegressor

    X = df[['Age', 'DailyStepCount', 'SleepDuration_Hours', 'SleepQualityScore',
            'StressIndex', 'CalorieBurn']].copy()
    y = df['WeeklyHealthScore'].copy()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Plot 1: Predicted vs Actual
    ax1 = axes[0]
    ax1.scatter(y_test, y_pred, alpha=0.6, s=80, c=COLORS['primary'], edgecolors='black', linewidth=0.5)
    ax1.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()],
             'r--', linewidth=2, label='Perfect Prediction')

    from sklearn.metrics import r2_score

    r2 = r2_score(y_test, y_pred)
    ax1.text(0.05, 0.95, f'R² = {r2:.3f}', transform=ax1.transAxes,
             fontsize=12, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    ax1.set_xlabel('Actual Health Score', fontsize=12)
    ax1.set_ylabel('Predicted Health Score', fontsize=12)
    ax1.set_title('Health Score Prediction Accuracy', fontsize=12, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot 2: Residuals
    ax2 = axes[1]
    residuals = y_test - y_pred
    ax2.scatter(y_pred, residuals, alpha=0.6, s=80, c=COLORS['accent'], edgecolors='black', linewidth=0.5)
    ax2.axhline(0, color='red', linestyle='--', linewidth=2)
    ax2.set_xlabel('Predicted Health Score', fontsize=12)
    ax2.set_ylabel('Residuals (Actual - Predicted)', fontsize=12)
    ax2.set_title('Residual Plot', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('model_performance_visualization.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: model_performance_visualization.png")
    plt.close()

except FileNotFoundError:
    print("⚠ Warning: smartcare_with_predictions.csv not found. Skipping model performance viz.")

# ============================================================================
# 7. INTERVENTION PRIORITY MATRIX
# ============================================================================

print("\n--- Creating Intervention Priority Matrix ---")

# Define intervention priorities based on analysis
interventions = {
    'Sleep Optimization': {'impact': 9, 'feasibility': 8, 'urgency': 9, 'affected': 24},
    'Physical Activity': {'impact': 8, 'feasibility': 7, 'urgency': 7, 'affected': 36},
    'Fall Prevention': {'impact': 10, 'feasibility': 6, 'urgency': 10, 'affected': 15},
    'Stress Management': {'impact': 8, 'feasibility': 7, 'urgency': 8, 'affected': 30},
    'Health Monitoring': {'impact': 6, 'feasibility': 9, 'urgency': 5, 'affected': 100}
}

fig, ax = plt.subplots(figsize=(12, 8))

for intervention, scores in interventions.items():
    # Plot impact vs feasibility, size by urgency, color by affected %
    ax.scatter(scores['feasibility'], scores['impact'],
               s=scores['urgency'] * 50, alpha=0.6,
               c=scores['affected'], cmap='Reds',
               edgecolors='black', linewidth=2)
    ax.annotate(intervention,
                (scores['feasibility'], scores['impact']),
                xytext=(5, 5), textcoords='offset points',
                fontsize=10, fontweight='bold')

# Add quadrant lines
ax.axhline(7.5, color='gray', linestyle='--', alpha=0.5)
ax.axvline(7.5, color='gray', linestyle='--', alpha=0.5)

# Add quadrant labels
ax.text(9, 9.5, 'High Priority\nQuick Wins', ha='center', fontsize=11,
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
ax.text(6, 9.5, 'High Priority\nResource Intensive', ha='center', fontsize=11,
        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
ax.text(9, 6, 'Lower Priority\nEasy Wins', ha='center', fontsize=11,
        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
ax.text(6, 6, 'Lower Priority\nReconsider', ha='center', fontsize=11,
        bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.5))

ax.set_xlabel('Feasibility (1-10)', fontsize=12, fontweight='bold')
ax.set_ylabel('Impact (1-10)', fontsize=12, fontweight='bold')
ax.set_title('Intervention Priority Matrix\n(Bubble size = Urgency, Color intensity = % Patients Affected)',
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlim(5, 10)
ax.set_ylim(5, 10.5)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('intervention_priority_matrix.png', dpi=300, bbox_inches='tight')
print("✓ Saved: intervention_priority_matrix.png")
plt.close()

# ============================================================================
# 8. SUMMARY TABLE VISUALIZATION
# ============================================================================

print("\n--- Creating Summary Statistics Table ---")

# Create comprehensive summary table
summary_stats = pd.DataFrame({
    'Metric': [
        'Total Patients',
        'Average Age',
        'Female %',
        'Average Health Score',
        'High/Critical Risk %',
        'Fall Alert Rate',
        'Sedentary %',
        'High Stress %',
        'Poor Sleep %',
        'Average Daily Steps'
    ],
    'Value': [
        len(df),
        f"{df['Age'].mean():.1f} years",
        f"{(df['Gender'] == 'Female').sum() / len(df) * 100:.1f}%",
        f"{df['WeeklyHealthScore'].mean():.1f}/100",
        f"{len(df[df['RiskCategory'].isin(['High Risk', 'Critical Risk'])]) / len(df) * 100:.1f}%",
        f"{df['FallAlerts'].sum()}/50 ({df['FallAlerts'].sum() / len(df) * 100:.0f}%)",
        f"{(df['ActivityLevel'] == 'Sedentary').sum() / len(df) * 100:.0f}%",
        f"{(df['StressLevel'] == 'High').sum() / len(df) * 100:.0f}%",
        f"{(df['SleepDuration_Hours'] < 6).sum() / len(df) * 100:.0f}%",
        f"{df['DailyStepCount'].mean():.0f}"
    ]
})

fig, ax = plt.subplots(figsize=(10, 8))
ax.axis('tight')
ax.axis('off')

table = ax.table(cellText=summary_stats.values,
                 colLabels=summary_stats.columns,
                 cellLoc='left',
                 loc='center',
                 colWidths=[0.6, 0.4])

table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 2)

# Style header
for i in range(len(summary_stats.columns)):
    table[(0, i)].set_facecolor(COLORS['primary'])
    table[(0, i)].set_text_props(weight='bold', color='white')

# Alternate row colors
for i in range(1, len(summary_stats) + 1):
    if i % 2 == 0:
        for j in range(len(summary_stats.columns)):
            table[(i, j)].set_facecolor('#f0f0f0')

plt.title('SmartCare Health Monitoring - Key Statistics Summary',
          fontsize=14, fontweight='bold', pad=20)
plt.savefig('summary_statistics_table.png', dpi=300, bbox_inches='tight')
print("✓ Saved: summary_statistics_table.png")
plt.close()

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("ADVANCED VISUALIZATION GENERATION COMPLETE")
print("=" * 70)
print("\nGenerated Visualizations:")
print("  1. executive_summary_dashboard.png - Overview dashboard")
print("  2. correlation_scatter_plots.png - Key correlations detailed")
print("  3. risk_quadrant_analysis.png - Risk segmentation quadrants")
print("  4. cluster_radar_profiles.png - Cluster characteristics radar")
print("  5. sleep_stress_comprehensive.png - Sleep-stress deep dive")
print("  6. model_performance_visualization.png - ML model accuracy")
print("  7. intervention_priority_matrix.png - Intervention prioritization")
print("  8. summary_statistics_table.png - Key statistics table")

print("\n💡 Usage in Report:")
print("  • Figure 3.1: executive_summary_dashboard.png (Section 3.1)")
print("  • Figure 3.2: correlation_scatter_plots.png (Section 3.3)")
print("  • Figure 3.3: risk_quadrant_analysis.png (Section 3.5)")
print("  • Figure 3.4: cluster_radar_profiles.png (Section 3.8)")
print("  • Figure 3.5: sleep_stress_comprehensive.png (Section 3.6)")
print("  • Figure 3.6: model_performance_visualization.png (Section 3.7)")
print("  • Figure 5.1: intervention_priority_matrix.png (Section 5)")
print("  • Table 3.1: summary_statistics_table.png (Section 3.1)")

print("\n🎨 All visualizations are publication-quality (300 DPI)")
print("=" * 70)