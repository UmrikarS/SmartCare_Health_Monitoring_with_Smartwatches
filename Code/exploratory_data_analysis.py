"""
SmartCare Health Monitoring Project - Phase 2
Exploratory Data Analysis (EDA)

Student: [Your Name]
Course: MBI806B
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
import openpyxl

warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("Set2")

print("=" * 70)
print("SMARTCARE EXPLORATORY DATA ANALYSIS")
print("=" * 70)

# Load cleaned data
df = pd.read_csv('smartcare_cleaned_data.csv')
print(f"\n✓ Data loaded: {len(df)} records, {len(df.columns)} variables")

# ============================================================================
# 1. DEMOGRAPHIC ANALYSIS
# ============================================================================

print("\n" + "=" * 70)
print("1. DEMOGRAPHIC CHARACTERISTICS")
print("=" * 70)

# Gender distribution
print("\nGender Distribution:")
gender_dist = df['Gender'].value_counts()
gender_pct = df['Gender'].value_counts(normalize=True) * 100
for gender in gender_dist.index:
    print(f"  {gender}: {gender_dist[gender]} ({gender_pct[gender]:.1f}%)")

# Age statistics by gender
print("\nAge Statistics by Gender:")
age_stats = df.groupby('Gender')['Age'].describe()
print(age_stats)

# Age group distribution
print("\nAge Group Distribution:")
age_group_dist = df['AgeGroup'].value_counts().sort_index()
for group in age_group_dist.index:
    count = age_group_dist[group]
    pct = (count / len(df)) * 100
    print(f"  {group}: {count} ({pct:.1f}%)")

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Demographic Overview', fontsize=16, fontweight='bold')

# Plot 1: Gender distribution
gender_counts = df['Gender'].value_counts()
axes[0, 0].pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%',
               startangle=90, colors=['#FF9999', '#66B2FF'])
axes[0, 0].set_title('Gender Distribution')

# Plot 2: Age distribution
axes[0, 1].hist(df['Age'], bins=15, color='steelblue', edgecolor='black', alpha=0.7)
axes[0, 1].set_xlabel('Age (years)')
axes[0, 1].set_ylabel('Frequency')
axes[0, 1].set_title('Age Distribution')
axes[0, 1].axvline(df['Age'].mean(), color='red', linestyle='--', label=f'Mean: {df["Age"].mean():.1f}')
axes[0, 1].legend()

# Plot 3: Age by Gender
df.boxplot(column='Age', by='Gender', ax=axes[1, 0])
axes[1, 0].set_title('Age Distribution by Gender')
axes[1, 0].set_xlabel('Gender')
axes[1, 0].set_ylabel('Age (years)')
plt.sca(axes[1, 0])
plt.xticks(rotation=0)

# Plot 4: Age Group distribution
age_group_order = ['50-59', '60-69', '70-79', '80+']
age_group_counts = df['AgeGroup'].value_counts().reindex(age_group_order)
axes[1, 1].bar(age_group_counts.index, age_group_counts.values, color='coral', edgecolor='black')
axes[1, 1].set_xlabel('Age Group')
axes[1, 1].set_ylabel('Count')
axes[1, 1].set_title('Patient Count by Age Group')
for i, v in enumerate(age_group_counts.values):
    axes[1, 1].text(i, v + 0.5, str(v), ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('demographic_analysis.png', dpi=300, bbox_inches='tight')
print("\n✓ Demographic visualization saved: 'demographic_analysis.png'")

# ============================================================================
# 2. HEALTH METRICS ANALYSIS
# ============================================================================

print("\n" + "=" * 70)
print("2. HEALTH METRICS OVERVIEW")
print("=" * 70)

health_metrics = ['DailyStepCount', 'HeartRate_Avg', 'SleepDuration_Hours',
                  'SleepQualityScore', 'StressIndex', 'CalorieBurn', 'WeeklyHealthScore']

print("\nHealth Metrics Summary Statistics:")
print(df[health_metrics].describe())

# Activity Level Analysis
print("\nActivity Level Distribution:")
activity_dist = df['ActivityLevel'].value_counts()
for level in ['Sedentary', 'Moderate', 'Active']:
    if level in activity_dist.index:
        count = activity_dist[level]
        pct = (count / len(df)) * 100
        print(f"  {level}: {count} ({pct:.1f}%)")

# Sleep Analysis
print("\nSleep Category Distribution:")
sleep_dist = df['SleepCategory'].value_counts()
for category in sleep_dist.index:
    count = sleep_dist[category]
    pct = (count / len(df)) * 100
    print(f"  {category}: {count} ({pct:.1f}%)")

# Stress Analysis
print("\nStress Level Distribution:")
stress_dist = df['StressLevel'].value_counts()
for level in ['Low', 'Moderate', 'High']:
    if level in stress_dist.index:
        count = stress_dist[level]
        pct = (count / len(df)) * 100
        print(f"  {level}: {count} ({pct:.1f}%)")

# Health Score Analysis
print("\nHealth Score Categories:")
health_dist = df['HealthCategory'].value_counts()
for category in ['Poor', 'Fair', 'Good', 'Excellent']:
    if category in health_dist.index:
        count = health_dist[category]
        pct = (count / len(df)) * 100
        print(f"  {category}: {count} ({pct:.1f}%)")

# Create health metrics visualization
fig, axes = plt.subplots(3, 3, figsize=(16, 14))
fig.suptitle('Health Metrics Distribution', fontsize=16, fontweight='bold')

metrics_to_plot = [
    ('DailyStepCount', 'Daily Steps', 'green'),
    ('HeartRate_Avg', 'Avg Heart Rate (bpm)', 'red'),
    ('SleepDuration_Hours', 'Sleep Duration (hours)', 'blue'),
    ('SleepQualityScore', 'Sleep Quality Score', 'purple'),
    ('StressIndex', 'Stress Index', 'orange'),
    ('CalorieBurn', 'Calorie Burn', 'brown'),
    ('WeeklyHealthScore', 'Weekly Health Score', 'darkgreen'),
    ('HeartRate_Range', 'Heart Rate Range', 'darkred'),
    ('Risk_Score', 'Risk Score', 'crimson')
]

for idx, (metric, label, color) in enumerate(metrics_to_plot):
    row = idx // 3
    col = idx % 3
    ax = axes[row, col]

    ax.hist(df[metric], bins=15, color=color, alpha=0.7, edgecolor='black')
    ax.set_xlabel(label)
    ax.set_ylabel('Frequency')
    ax.set_title(f'{label} Distribution')

    # Add mean line
    mean_val = df[metric].mean()
    ax.axvline(mean_val, color='black', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.1f}')
    ax.legend()

plt.tight_layout()
plt.savefig('health_metrics_distribution.png', dpi=300, bbox_inches='tight')
print("\n✓ Health metrics visualization saved: 'health_metrics_distribution.png'")

# ============================================================================
# 3. CORRELATION ANALYSIS
# ============================================================================

print("\n" + "=" * 70)
print("3. CORRELATION ANALYSIS")
print("=" * 70)

# Select numeric columns for correlation
numeric_cols = ['Age', 'DailyStepCount', 'HeartRate_Min', 'HeartRate_Max',
                'HeartRate_Avg', 'SleepDuration_Hours', 'SleepQualityScore',
                'StressIndex', 'CalorieBurn', 'WeeklyHealthScore', 'Risk_Score']

correlation_matrix = df[numeric_cols].corr()

print("\nTop 10 Strongest Correlations (excluding diagonal):")
# Get upper triangle of correlation matrix
mask = np.triu(np.ones_like(correlation_matrix), k=1).astype(bool)
corr_pairs = correlation_matrix.where(mask).stack().reset_index()
corr_pairs.columns = ['Variable1', 'Variable2', 'Correlation']
corr_pairs['Abs_Correlation'] = corr_pairs['Correlation'].abs()
top_correlations = corr_pairs.nlargest(10, 'Abs_Correlation')

for idx, row in top_correlations.iterrows():
    print(f"  {row['Variable1']} <-> {row['Variable2']}: r = {row['Correlation']:.3f}")

# Key findings
print("\nKey Correlation Insights:")
sleep_stress_corr = correlation_matrix.loc['SleepDuration_Hours', 'StressIndex']
print(f"  • Sleep Duration & Stress Index: r = {sleep_stress_corr:.3f}")
print(f"    {'Strong inverse relationship' if sleep_stress_corr < -0.5 else 'Moderate inverse relationship'}")

steps_health_corr = correlation_matrix.loc['DailyStepCount', 'WeeklyHealthScore']
print(f"  • Daily Steps & Health Score: r = {steps_health_corr:.3f}")
print(f"    {'Positive association' if steps_health_corr > 0 else 'Negative association'}")

sleep_quality_corr = correlation_matrix.loc['SleepQualityScore', 'WeeklyHealthScore']
print(f"  • Sleep Quality & Health Score: r = {sleep_quality_corr:.3f}")

# Create correlation heatmap
plt.figure(figsize=(14, 10))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='RdYlGn',
            center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Correlation Heatmap - Health Metrics', fontsize=16, fontweight='bold', pad=20)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
print("\n✓ Correlation heatmap saved: 'correlation_heatmap.png'")

# ============================================================================
# 4. AGE GROUP ANALYSIS
# ============================================================================

print("\n" + "=" * 70)
print("4. AGE GROUP TRENDS")
print("=" * 70)

# Metrics by age group
age_group_stats = df.groupby('AgeGroup')[health_metrics].mean()
print("\nAverage Health Metrics by Age Group:")
print(age_group_stats.round(2))

# Statistical testing - ANOVA for age group differences
print("\nANOVA Tests for Age Group Differences:")
for metric in ['WeeklyHealthScore', 'StressIndex', 'SleepDuration_Hours', 'DailyStepCount']:
    groups = [df[df['AgeGroup'] == group][metric].values for group in age_group_order]
    f_stat, p_value = stats.f_oneway(*groups)
    significance = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else "ns"
    print(f"  {metric}: F={f_stat:.3f}, p={p_value:.4f} {significance}")

# Visualize age group trends
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Health Metrics Trends by Age Group', fontsize=16, fontweight='bold')

metrics_to_compare = [
    ('WeeklyHealthScore', 'Weekly Health Score', 'green'),
    ('StressIndex', 'Stress Index', 'orange'),
    ('DailyStepCount', 'Daily Step Count', 'blue'),
    ('SleepDuration_Hours', 'Sleep Duration (hours)', 'purple')
]

for idx, (metric, label, color) in enumerate(metrics_to_compare):
    row = idx // 2
    col = idx % 2
    ax = axes[row, col]

    # Box plot
    df.boxplot(column=metric, by='AgeGroup', ax=ax)
    ax.set_title(f'{label} by Age Group')
    ax.set_xlabel('Age Group')
    ax.set_ylabel(label)
    plt.sca(ax)
    plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig('age_group_trends.png', dpi=300, bbox_inches='tight')
print("\n✓ Age group trends saved: 'age_group_trends.png'")

# ============================================================================
# 5. GENDER COMPARISON ANALYSIS
# ============================================================================

print("\n" + "=" * 70)
print("5. GENDER COMPARISON")
print("=" * 70)

# Metrics by gender
gender_stats = df.groupby('Gender')[health_metrics].mean()
print("\nAverage Health Metrics by Gender:")
print(gender_stats.round(2))

# T-tests for gender differences
print("\nIndependent T-Tests for Gender Differences:")
for metric in health_metrics:
    male_data = df[df['Gender'] == 'Male'][metric]
    female_data = df[df['Gender'] == 'Female'][metric]
    t_stat, p_value = stats.ttest_ind(male_data, female_data)
    significance = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else "ns"
    print(f"  {metric}: t={t_stat:.3f}, p={p_value:.4f} {significance}")

# Gender comparison visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Health Metrics Comparison by Gender', fontsize=16, fontweight='bold')

for idx, (metric, label, color) in enumerate(metrics_to_compare):
    row = idx // 2
    col = idx % 2
    ax = axes[row, col]

    # Violin plot
    gender_data = [df[df['Gender'] == 'Male'][metric], df[df['Gender'] == 'Female'][metric]]
    parts = ax.violinplot(gender_data, positions=[1, 2], showmeans=True, showmedians=True)
    ax.set_xticks([1, 2])
    ax.set_xticklabels(['Male', 'Female'])
    ax.set_ylabel(label)
    ax.set_title(f'{label} by Gender')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('gender_comparison.png', dpi=300, bbox_inches='tight')
print("\n✓ Gender comparison saved: 'gender_comparison.png'")

# ============================================================================
# 6. FALL ALERT ANALYSIS
# ============================================================================

print("\n" + "=" * 70)
print("6. FALL ALERT RISK FACTORS")
print("=" * 70)

# Fall alert statistics
fall_count = df['FallAlerts'].sum()
fall_pct = (fall_count / len(df)) * 100
print(f"\nPatients with Fall Alerts: {fall_count} ({fall_pct:.1f}%)")

# Characteristics of fall alert patients
fall_patients = df[df['FallAlerts'] == 1]
no_fall_patients = df[df['FallAlerts'] == 0]

print("\nFall Alert Patients Characteristics:")
print(f"  Average Age: {fall_patients['Age'].mean():.1f} vs {no_fall_patients['Age'].mean():.1f} (no falls)")
print(
    f"  Average Steps: {fall_patients['DailyStepCount'].mean():.0f} vs {no_fall_patients['DailyStepCount'].mean():.0f}")
print(
    f"  Average Sleep: {fall_patients['SleepDuration_Hours'].mean():.1f} vs {no_fall_patients['SleepDuration_Hours'].mean():.1f} hours")
print(
    f"  Average Health Score: {fall_patients['WeeklyHealthScore'].mean():.1f} vs {no_fall_patients['WeeklyHealthScore'].mean():.1f}")

# Age group distribution for falls
print("\nFall Alerts by Age Group:")
fall_by_age = df.groupby('AgeGroup')['FallAlerts'].agg(['sum', 'count'])
fall_by_age['percentage'] = (fall_by_age['sum'] / fall_by_age['count'] * 100)
for age_group in age_group_order:
    if age_group in fall_by_age.index:
        falls = fall_by_age.loc[age_group, 'sum']
        total = fall_by_age.loc[age_group, 'count']
        pct = fall_by_age.loc[age_group, 'percentage']
        print(f"  {age_group}: {falls}/{total} ({pct:.1f}%)")

# Activity level and falls
print("\nFall Alerts by Activity Level:")
fall_by_activity = df.groupby('ActivityLevel')['FallAlerts'].agg(['sum', 'count'])
fall_by_activity['percentage'] = (fall_by_activity['sum'] / fall_by_activity['count'] * 100)
for level in ['Sedentary', 'Moderate', 'Active']:
    if level in fall_by_activity.index:
        falls = fall_by_activity.loc[level, 'sum']
        total = fall_by_activity.loc[level, 'count']
        pct = fall_by_activity.loc[level, 'percentage']
        print(f"  {level}: {falls}/{total} ({pct:.1f}%)")

# Fall alert visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Fall Alert Risk Factor Analysis', fontsize=16, fontweight='bold')

# Plot 1: Age distribution
axes[0, 0].hist([no_fall_patients['Age'], fall_patients['Age']],
                bins=15, label=['No Falls', 'Falls'], alpha=0.7, color=['green', 'red'])
axes[0, 0].set_xlabel('Age')
axes[0, 0].set_ylabel('Frequency')
axes[0, 0].set_title('Age Distribution by Fall Status')
axes[0, 0].legend()

# Plot 2: Activity level
axes[0, 1].hist([no_fall_patients['DailyStepCount'], fall_patients['DailyStepCount']],
                bins=15, label=['No Falls', 'Falls'], alpha=0.7, color=['green', 'red'])
axes[0, 1].set_xlabel('Daily Step Count')
axes[0, 1].set_ylabel('Frequency')
axes[0, 1].set_title('Activity Level by Fall Status')
axes[0, 1].legend()

# Plot 3: Sleep duration
axes[1, 0].hist([no_fall_patients['SleepDuration_Hours'], fall_patients['SleepDuration_Hours']],
                bins=10, label=['No Falls', 'Falls'], alpha=0.7, color=['green', 'red'])
axes[1, 0].set_xlabel('Sleep Duration (hours)')
axes[1, 0].set_ylabel('Frequency')
axes[1, 0].set_title('Sleep Duration by Fall Status')
axes[1, 0].legend()

# Plot 4: Health score
axes[1, 1].hist([no_fall_patients['WeeklyHealthScore'], fall_patients['WeeklyHealthScore']],
                bins=15, label=['No Falls', 'Falls'], alpha=0.7, color=['green', 'red'])
axes[1, 1].set_xlabel('Weekly Health Score')
axes[1, 1].set_ylabel('Frequency')
axes[1, 1].set_title('Health Score by Fall Status')
axes[1, 1].legend()

plt.tight_layout()
plt.savefig('fall_alert_analysis.png', dpi=300, bbox_inches='tight')
print("\n✓ Fall alert analysis saved: 'fall_alert_analysis.png'")

# ============================================================================
# 7. RISK SEGMENTATION ANALYSIS
# ============================================================================

print("\n" + "=" * 70)
print("7. PATIENT RISK SEGMENTATION")
print("=" * 70)

# Risk category distribution
print("\nRisk Category Distribution:")
risk_dist = df['RiskCategory'].value_counts()
for category in ['Low Risk', 'Medium Risk', 'High Risk', 'Critical Risk']:
    if category in risk_dist.index:
        count = risk_dist[category]
        pct = (count / len(df)) * 100
        print(f"  {category}: {count} ({pct:.1f}%)")

# Risk profile by age group
print("\nRisk Distribution by Age Group:")
risk_by_age = pd.crosstab(df['AgeGroup'], df['RiskCategory'], normalize='index') * 100
print(risk_by_age.round(1))

# High-risk patient characteristics
high_risk = df[df['RiskCategory'].isin(['High Risk', 'Critical Risk'])]
print(f"\nHigh-Risk Patient Profile (n={len(high_risk)}):")
print(f"  Average Age: {high_risk['Age'].mean():.1f} years")
print(f"  Average Steps: {high_risk['DailyStepCount'].mean():.0f}")
print(f"  Average Sleep: {high_risk['SleepDuration_Hours'].mean():.1f} hours")
print(f"  Average Stress: {high_risk['StressIndex'].mean():.1f}")
print(f"  Average Health Score: {high_risk['WeeklyHealthScore'].mean():.1f}")
print(f"  Fall Alert Rate: {(high_risk['FallAlerts'].sum() / len(high_risk) * 100):.1f}%")

# Risk segmentation visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Patient Risk Segmentation Analysis', fontsize=16, fontweight='bold')

# Plot 1: Risk category pie chart
risk_counts = df['RiskCategory'].value_counts()
colors = ['#2ecc71', '#f39c12', '#e74c3c', '#8e44ad']
axes[0, 0].pie(risk_counts, labels=risk_counts.index, autopct='%1.1f%%',
               startangle=90, colors=colors)
axes[0, 0].set_title('Risk Category Distribution')

# Plot 2: Risk score distribution
axes[0, 1].hist(df['Risk_Score'], bins=20, color='crimson', alpha=0.7, edgecolor='black')
axes[0, 1].set_xlabel('Risk Score')
axes[0, 1].set_ylabel('Frequency')
axes[0, 1].set_title('Risk Score Distribution')
axes[0, 1].axvline(df['Risk_Score'].mean(), color='blue', linestyle='--',
                   linewidth=2, label=f'Mean: {df["Risk_Score"].mean():.1f}')
axes[0, 1].legend()

# Plot 3: Risk by age group
risk_age_counts = df.groupby(['AgeGroup', 'RiskCategory']).size().unstack(fill_value=0)
risk_age_counts.plot(kind='bar', stacked=True, ax=axes[1, 0], color=colors)
axes[1, 0].set_xlabel('Age Group')
axes[1, 0].set_ylabel('Patient Count')
axes[1, 0].set_title('Risk Categories by Age Group')
axes[1, 0].legend(title='Risk Category', bbox_to_anchor=(1.05, 1), loc='upper left')
axes[1, 0].set_xticklabels(axes[1, 0].get_xticklabels(), rotation=0)

# Plot 4: Risk score vs Health score scatter
colors_map = {'Low Risk': '#2ecc71', 'Medium Risk': '#f39c12',
              'High Risk': '#e74c3c', 'Critical Risk': '#8e44ad'}
for category in df['RiskCategory'].unique():
    mask = df['RiskCategory'] == category
    axes[1, 1].scatter(df[mask]['WeeklyHealthScore'], df[mask]['Risk_Score'],
                       label=category, alpha=0.6, s=50, color=colors_map.get(category, 'gray'))
axes[1, 1].set_xlabel('Weekly Health Score')
axes[1, 1].set_ylabel('Risk Score')
axes[1, 1].set_title('Risk Score vs Health Score')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('risk_segmentation.png', dpi=300, bbox_inches='tight')
print("\n✓ Risk segmentation saved: 'risk_segmentation.png'")

# ============================================================================
# 8. SLEEP-STRESS RELATIONSHIP
# ============================================================================

print("\n" + "=" * 70)
print("8. SLEEP-STRESS CORRELATION ANALYSIS")
print("=" * 70)

# Detailed sleep-stress analysis
sleep_stress_corr = df['SleepDuration_Hours'].corr(df['StressIndex'])
print(f"\nPearson Correlation: r = {sleep_stress_corr:.3f}")

# Regression analysis
from scipy.stats import linregress

slope, intercept, r_value, p_value, std_err = linregress(df['SleepDuration_Hours'], df['StressIndex'])
print(f"Linear Regression: StressIndex = {intercept:.2f} + {slope:.2f} * SleepDuration")
print(f"R² = {r_value ** 2:.3f}, p-value = {p_value:.4f}")

# Sleep category vs stress levels
print("\nAverage Stress by Sleep Category:")
stress_by_sleep = df.groupby('SleepCategory')['StressIndex'].agg(['mean', 'std', 'count'])
print(stress_by_sleep.round(2))

# Create sleep-stress visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Sleep Duration and Stress Index Relationship', fontsize=16, fontweight='bold')

# Plot 1: Scatter plot with regression line
axes[0, 0].scatter(df['SleepDuration_Hours'], df['StressIndex'], alpha=0.6, color='purple')
x_line = np.linspace(df['SleepDuration_Hours'].min(), df['SleepDuration_Hours'].max(), 100)
y_line = intercept + slope * x_line
axes[0, 0].plot(x_line, y_line, color='red', linewidth=2,
                label=f'y = {intercept:.1f} + {slope:.1f}x\nR² = {r_value ** 2:.3f}')
axes[0, 0].set_xlabel('Sleep Duration (hours)')
axes[0, 0].set_ylabel('Stress Index')
axes[0, 0].set_title('Sleep vs Stress Correlation')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Plot 2: Box plot by sleep category
sleep_categories_ordered = ['Poor', 'Fair', 'Good', 'Excessive']
sleep_data = [df[df['SleepCategory'] == cat]['StressIndex'].values
              for cat in sleep_categories_ordered if cat in df['SleepCategory'].unique()]
axes[0, 1].boxplot(sleep_data, labels=[cat for cat in sleep_categories_ordered
                                       if cat in df['SleepCategory'].unique()])
axes[0, 1].set_xlabel('Sleep Category')
axes[0, 1].set_ylabel('Stress Index')
axes[0, 1].set_title('Stress Levels by Sleep Category')
axes[0, 1].grid(True, alpha=0.3)

# Plot 3: Sleep distribution by stress level
stress_levels_ordered = ['Low', 'Moderate', 'High']
sleep_by_stress = [df[df['StressLevel'] == level]['SleepDuration_Hours'].values
                   for level in stress_levels_ordered if level in df['StressLevel'].unique()]
axes[1, 0].boxplot(sleep_by_stress, labels=[level for level in stress_levels_ordered
                                            if level in df['StressLevel'].unique()])
axes[1, 0].set_xlabel('Stress Level')
axes[1, 0].set_ylabel('Sleep Duration (hours)')
axes[1, 0].set_title('Sleep Duration by Stress Level')
axes[1, 0].grid(True, alpha=0.3)

# Plot 4: Heatmap of sleep-stress combinations
sleep_stress_pivot = pd.crosstab(df['SleepCategory'], df['StressLevel'])
sns.heatmap(sleep_stress_pivot, annot=True, fmt='d', cmap='YlOrRd', ax=axes[1, 1])
axes[1, 1].set_title('Patient Count: Sleep Category vs Stress Level')
axes[1, 1].set_xlabel('Stress Level')
axes[1, 1].set_ylabel('Sleep Category')

plt.tight_layout()
plt.savefig('sleep_stress_analysis.png', dpi=300, bbox_inches='tight')
print("\n✓ Sleep-stress analysis saved: 'sleep_stress_analysis.png'")

# ============================================================================
# 9. SUMMARY STATISTICS EXPORT
# ============================================================================

print("\n" + "=" * 70)
print("9. EXPORTING SUMMARY STATISTICS")
print("=" * 70)

# Create comprehensive summary report
summary_stats = {
    'Overall': df[health_metrics].describe().T,
    'By_Gender': df.groupby('Gender')[health_metrics].mean(),
    'By_AgeGroup': df.groupby('AgeGroup')[health_metrics].mean(),
    'By_RiskCategory': df.groupby('RiskCategory')[health_metrics].mean()
}

# Export to Excel
with pd.ExcelWriter('eda_summary_statistics.xlsx', engine='openpyxl') as writer:
    summary_stats['Overall'].to_excel(writer, sheet_name='Overall Statistics')
    summary_stats['By_Gender'].to_excel(writer, sheet_name='By Gender')
    summary_stats['By_AgeGroup'].to_excel(writer, sheet_name='By Age Group')
    summary_stats['By_RiskCategory'].to_excel(writer, sheet_name='By Risk Category')

    # Correlation matrix
    correlation_matrix.to_excel(writer, sheet_name='Correlations')

print("\n✓ Summary statistics exported: 'eda_summary_statistics.xlsx'")

# ============================================================================
# 10. KEY INSIGHTS SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("KEY INSIGHTS FROM EXPLORATORY ANALYSIS")
print("=" * 70)

print("\n1. DEMOGRAPHIC INSIGHTS:")
print(f"   • Gender distribution: {gender_dist['Female']} Female, {gender_dist['Male']} Male")
print(f"   • Age range: {df['Age'].min()}-{df['Age'].max()} years (mean: {df['Age'].mean():.1f})")
print(f"   • Most common age group: {df['AgeGroup'].value_counts().index[0]}")

print("\n2. HEALTH STATUS:")
print(f"   • Average health score: {df['WeeklyHealthScore'].mean():.1f}/100")
print(f"   • High-risk patients: {len(high_risk)} ({len(high_risk) / len(df) * 100:.1f}%)")
print(f"   • Fall alert incidence: {fall_pct:.1f}%")

print("\n3. ACTIVITY PATTERNS:")
print(f"   • Average daily steps: {df['DailyStepCount'].mean():.0f}")
print(
    f"   • Sedentary patients: {activity_dist.get('Sedentary', 0)} ({activity_dist.get('Sedentary', 0) / len(df) * 100:.1f}%)")
print(f"   • Active patients: {activity_dist.get('Active', 0)} ({activity_dist.get('Active', 0) / len(df) * 100:.1f}%)")

print("\n4. SLEEP & STRESS:")
print(f"   • Average sleep duration: {df['SleepDuration_Hours'].mean():.1f} hours")
print(f"   • Average stress index: {df['StressIndex'].mean():.1f}/100")
print(f"   • Sleep-stress correlation: r = {sleep_stress_corr:.3f} (strong inverse)")

print("\n5. RISK FACTORS:")
print(f"   • Sleep duration < 6h: {len(df[df['SleepDuration_Hours'] < 6])} patients")
print(f"   • High stress (>70): {len(df[df['StressIndex'] > 70])} patients")
print(f"   • Low activity (<5000 steps): {len(df[df['DailyStepCount'] < 5000])} patients")

print("\n" + "=" * 70)
print("EXPLORATORY DATA ANALYSIS COMPLETE")
print("=" * 70)
print("\nGenerated Outputs:")
print("  1. demographic_analysis.png")
print("  2. health_metrics_distribution.png")
print("  3. correlation_heatmap.png")
print("  4. age_group_trends.png")
print("  5. gender_comparison.png")
print("  6. fall_alert_analysis.png")
print("  7. risk_segmentation.png")
print("  8. sleep_stress_analysis.png")
print("  9. eda_summary_statistics.xlsx")
print("\nNext Steps:")
print("  • Build predictive models")
print("  • Perform clustering analysis")
print("  • Create interactive dashboards")
print("=" * 70)