import warnings

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set visualization style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("="*70)
print("SMARTCARE DATA PREPROCESSING & CLEANING")
print("="*70)

# =========================================================================
# 1. DATA LOADING
# =========================================================================

# Load the dataset
df = pd.read_csv("smartwatch_health_data.csv")

print("Dataset loaded successfully")
print(f"Records: {len(df)}")
print(f"Variables: {len(df.columns)}")

# =========================================================================
# 2. INITIAL DATA INSPECTION
# =========================================================================

print("\n"+"="*70)
print("DATA QUALITY ASSESSMENT")
print("="*70)

# Display first few records
print("\nFirst 5 records")
print(df.head())

# Data types
print("\nData Types: ")
print(df.dtypes)

# Summary statistics
print("\nDescriptive Statistics: ")
print(df.describe())

# Missing values check
print("\nMissing Values Check: ")
missing = df.isnull().sum()
print(missing)
if missing.sum() == 0:
    print("No missing values detected")

# Duplicate check
duplicates = df.duplicated().sum()
print(f"\nDuplicate Records: {duplicates}")
if duplicates == 0:
    print("No duplicate records found")

# =========================================================================
# 3. DATA PREPROCESSING & FEATURE ENGINEERING
# =========================================================================

print("\n" + "="*70)
print("FEATURE ENGINEERING")
print("="*70)

# Create a copy for processing
df_clean = df.copy()

# 3.1 Age Groups
def categorize_age(age):
    if age < 60:
        return '50-59'
    elif age < 70:
        return '60-69'
    elif age < 80:
        return '70-79'
    else:
        return '80+'

df_clean['AgeGroup'] = df_clean['Age'].apply(categorize_age)
print("\nAge groups created")
print(df_clean['AgeGroup'].value_counts().sort_index())

# 3.2 Activity Level Classification
def categorize_activity(steps):
    if steps < 5000:
        return 'Sedentary'
    elif steps < 10000:
        return 'Moderate'
    else:
        return "Active"

df_clean['ActivityLevel'] = df_clean['DailyStepCount'].apply(categorize_activity)
print("\nActivity levels created")
print(df_clean['ActivityLevel'].value_counts())

# 3.3 Sleep Quality Categories
def categorize_sleep_duration(hours):
    if hours < 6:
        return 'Poor'
    elif hours < 7:
        return 'Fair'
    elif hours <= 9:
        return 'Good'
    else:
        return 'Excessive'

df_clean['SleepCategory'] = df_clean['SleepDuration_Hours'].apply(categorize_sleep_duration)
print("\n Sleep categories created")
print(df_clean['SleepCategory'].value_counts())

# 3.4 Heart Rate Variability
df_clean['HeartRate_Range'] = df_clean['HeartRate_Max'] - df_clean['HeartRate_Min']
print("\nHeart Rate Range calculated")
print(f"Mean HR Range: {df_clean['HeartRate_Range'].mean():.2f} bpm")

# 3.5 Stress Level Categories
def categorize_stress(stress):
    if stress < 40:
        return 'Low'
    elif stress < 70:
        return 'Moderate'
    else:
        return 'High'

df_clean['StressLevel'] = df_clean['StressIndex'].apply(categorize_stress)
print("\nStress levels created:")
print(df_clean['StressLevel'].value_counts())

# 3.6 Health Score Categories
def categorize_health_score(score):
    if score < 60:
        return 'Poor'
    elif score < 75:
        return 'Fair'
    elif score < 90:
        return 'Good'
    else:
        return 'Excellent'

df_clean['HealthCategory'] = df_clean['WeeklyHealthScore'].apply(categorize_health_score)
print("\nHealth categories created:")
print(df_clean['HealthCategory'].value_counts())

# 3.7 Composite Risk Score
# Normalize and weight different factors
df_clean['Risk_Score'] = (
    (100 - df_clean['WeeklyHealthScore']) * 0.3 + # Lower health score = higher risk
    df_clean['StressIndex'] * 0.2 + # Higher stress = higher risk
    (10 - df_clean['SleepDuration_Hours']) * 5 * 0.2 + # Poor sleep = higher risk
    (15000 - df_clean['DailyStepCount']) / 100 * 0.2 + # Low activity = higher risk
    df_clean['FallAlerts'] * 20 * 0.1 # Fall history = higher risk
)

# Normalize Risk Score from 0 to 100
df_clean['Risk_Score'] = (df_clean['Risk_Score'] - df_clean['Risk_Score'].min()) / \
                         (df_clean['Risk_Score'].max() - df_clean['Risk_Score'].min()) * 100
print("\nComposite Risk Score created")
print(f"Mean Risk Score: {df_clean['Risk_Score'].mean():.2f}")
print(f"Risk Score Range: {df_clean['Risk_Score'].min():.2f} - {df_clean['Risk_Score'].max():.2f}")

# 3.8 Risk Categories
def categorize_risk(risk_score):
    if risk_score < 25:
        return 'Low Risk'
    elif risk_score < 50:
        return 'Medium Risk'
    elif risk_score < 75:
        return 'High Risk'
    else:
        return 'Critical Risk'

df_clean['RiskCategory'] = df_clean['Risk_Score'].apply(categorize_risk)
print("\n✓ Risk categories created:")
print(df_clean['RiskCategory'].value_counts())

# ============================================================================
# 4. OUTLIER DETECTION
# ============================================================================

print("\n" + "="*70)
print("OUTLIER DETECTION (IQR Method)")
print("="*70)

numeric_cols = ['Age', 'DailyStepCount', 'HeartRate_Min', 'HeartRate_Max',
                'HeartRate_Avg', 'SleepDuration_Hours', 'SleepQualityScore',
                'StressIndex', 'CalorieBurn', 'WeeklyHealthScore']

outliers_summary = []

for col in numeric_cols:
    Q1 = df_clean[col].quantile(0.25)
    Q3 = df_clean[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df_clean[(df_clean[col] < lower_bound)] | (df_clean[col] > upper_bound)
    outlier_count = len(outliers)

    if outlier_count > 0:
        outliers_summary.append({
            'Variable':  col,
            'Outliers': outlier_count,
            'Lower Bound': f"{lower_bound:.2f}",
            'Upper Bound': f"{upper_bound:.2f}",
            'Action': 'Retained (clinically plausible)'
        })

if outliers_summary:
    outliers_df = pd.DataFrame(outliers_summary)
    print("\nOutliers Detected:")
    print(outliers_df.to_string(index=False))
    print("\n✓ Decision: All outliers retained as they represent genuine patient variation")
else:
    print("\n✓ No significant outliers detected")

# ============================================================================
# 5. DATA VALIDATION
# ============================================================================

print("\n" + "="*70)
print("DATA VALIDATION")
print("="*70)

validation_checks = []

# Check 1: Age range
age_valid = df_clean['Age'].between(50, 100).all()
validation_checks.append(('Age Range (50-100)', age_valid))

# Check 2: Heart Rate validity
hr_valid = (df_clean['HeartRate_Min'] < df_clean['HeartRate_Max']).all()
validation_checks.append(('HR Min < HR Max', hr_valid))

# Check 3: Sleep duration
sleep_valid = df_clean['SleepDuration_Hours'].between(0, 12).all()
validation_checks.append(('Sleep Duration (0-12h)', sleep_valid))

# Check 4: Stress Index
stress_valid = df_clean['StressIndex'].between(0, 100).all()
validation_checks.append(('Stress Index (0-100)', stress_valid))

# Check 5: Fall Alerts
fall_valid = df_clean['FallAlerts'].isin([0, 1]).all()
validation_checks.append(('Fall Alerts (0/1)', fall_valid))

# Check 6: Health Score
health_valid = df_clean['WeeklyHealthScore'].between(0, 100).all()
validation_checks.append(('Health Score (0-100)', health_valid))

print("\nValidation Results:")
for check, result in validation_checks:
    status = "✓ PASS" if result else "✗ FAIL"
    print(f"  {check}: {status}")

all_valid = all([result for _, result in validation_checks])
if all_valid:
    print("\n✓ All validation checks passed")

# ============================================================================
# 6. SAVE PROCESSED DATA
# ============================================================================

print("\n" + "="*70)
print("DATA EXPORT")
print("="*70)

# Save cleaned dataset
df_clean.to_csv('smartcare_cleaned_data.csv', index=False)
print("\n✓ Cleaned dataset saved: 'smartcare_cleaned_data.csv'")

# Create summary report
summary_report = {
    'Total Records': len(df_clean),
    'Total Variables': len(df_clean.columns),
    'Original Variables': len(df.columns),
    'Engineered Features': len(df_clean.columns) - len(df.columns),
    'Missing Values': df_clean.isnull().sum().sum(),
    'Duplicates': df_clean.duplicated().sum(),
    'Age Range': f"{df_clean['Age'].min()}-{df_clean['Age'].max()}",
    'Gender Distribution': df_clean['Gender'].value_counts().to_dict(),
    'Fall Alerts': df_clean['FallAlerts'].sum()
}

print("\nData Summary:")
for key, value in summary_report.items():
    print(f"  {key}: {value}")

print("\n" + "="*70)
print("PREPROCESSING COMPLETE")
print("="*70)
print("\nNext Steps:")
print("  1. Run exploratory data analysis (EDA)")
print("  2. Perform correlation analysis")
print("  3. Conduct statistical testing")
print("  4. Build predictive models")
print("="*70)