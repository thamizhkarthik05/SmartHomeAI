import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load and analyze the dataset
df = pd.read_csv('SmartHome_Environment_v1.csv')

print("="*60)
print("DATASET VALIDATION REPORT")
print("="*60)

# 1. Basic Information
print("\n1. DATASET OVERVIEW")
print("-"*40)
print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"Date range: {df['timestamp'].iloc[0]} to {df['timestamp'].iloc[-1]}")
print(f"Duration: ~{len(df) / 1440:.1f} days ({len(df) / 60:.0f} hours)")

# 2. Check for missing values
print("\n2. DATA QUALITY CHECK")
print("-"*40)
missing_values = df.isnull().sum()
print("Missing values per column:")
for col, missing in missing_values.items():
    print(f"  {col}: {missing} ({missing/len(df)*100:.2f}%)")

# 3. Data Statistics
print("\n3. DATA STATISTICS")
print("-"*40)
print(df[['room_temperature_c', 'perceived_temperature_c', 'ambient_light_lux', 
          'comfort_score', 'light_state_percent', 'energy_consumed_kw']].describe())

# 4. Check for variability (critical for RL training)
print("\n4. DATA VARIABILITY ANALYSIS")
print("-"*40)
print(f"Temperature range: {df['room_temperature_c'].min():.2f}°C to {df['room_temperature_c'].max():.2f}°C")
print(f"Temperature variance: {df['room_temperature_c'].var():.4f}")
print(f"Light range: {df['ambient_light_lux'].min():.0f} to {df['ambient_light_lux'].max():.0f} lux")
print(f"Light variance: {df['ambient_light_lux'].var():.2f}")
print(f"Comfort range: {df['comfort_score'].min():.4f} to {df['comfort_score'].max():.4f}")
print(f"Comfort variance: {df['comfort_score'].var():.6f}")
print(f"Energy range: {df['energy_consumed_kw'].min():.2f} to {df['energy_consumed_kw'].max():.2f} kW")

# 5. Check different times of day
print("\n5. TEMPORAL PATTERNS CHECK")
print("-"*40)
df['hour'] = pd.to_datetime(df['timestamp'], dayfirst=True).dt.hour

morning = df[df['hour'].between(6, 11)]
afternoon = df[df['hour'].between(12, 17)]
evening = df[df['hour'].between(18, 22)]
night = df[(df['hour'] >= 23) | (df['hour'] <= 5)]

print("Morning (6-11 AM):")
print(f"  Avg temp: {morning['room_temperature_c'].mean():.2f}°C, Avg light: {morning['ambient_light_lux'].mean():.0f} lux, Avg comfort: {morning['comfort_score'].mean():.3f}")
print("Afternoon (12-5 PM):")
print(f"  Avg temp: {afternoon['room_temperature_c'].mean():.2f}°C, Avg light: {afternoon['ambient_light_lux'].mean():.0f} lux, Avg comfort: {afternoon['comfort_score'].mean():.3f}")
print("Evening (6-10 PM):")
print(f"  Avg temp: {evening['room_temperature_c'].mean():.2f}°C, Avg light: {evening['ambient_light_lux'].mean():.0f} lux, Avg comfort: {evening['comfort_score'].mean():.3f}")
print("Night (11 PM-5 AM):")
print(f"  Avg temp: {night['room_temperature_c'].mean():.2f}°C, Avg light: {night['ambient_light_lux'].mean():.0f} lux, Avg comfort: {night['comfort_score'].mean():.3f}")

# 6. Check occupancy patterns
print("\n6. OCCUPANCY PATTERNS")
print("-"*40)
occupied = df[df['is_occupied'] == True]
unoccupied = df[df['is_occupied'] == False]
print(f"Occupied time: {len(occupied)/len(df)*100:.1f}%")
print(f"Unoccupied time: {len(unoccupied)/len(df)*100:.1f}%")

# 7. Check user overrides
print("\n7. USER OVERRIDE EVENTS")
print("-"*40)
overrides = df[df['user_override_event'] == True]
print(f"Total overrides: {len(overrides)} ({len(overrides)/len(df)*100:.2f}%)")
if len(overrides) > 0:
    print(f"Avg temp during override: {overrides['room_temperature_c'].mean():.2f}°C")
    print(f"Avg comfort during override: {overrides['comfort_score'].mean():.3f}")

# 8. Critical Issues Check
print("\n8. CRITICAL ISSUES IDENTIFICATION")
print("-"*40)
issues = []

# Check if data is too static
if df['room_temperature_c'].var() < 1.0:
    issues.append("⚠️ CRITICAL: Temperature variance is very low (< 1.0) - data may be too static!")

if df['comfort_score'].var() < 0.01:
    issues.append("⚠️ CRITICAL: Comfort score variance is very low - AI won't learn meaningful patterns!")

if df['ambient_light_lux'].var() < 1000:
    issues.append("⚠️ WARNING: Light variation is low - limited learning opportunities!")

# Check if comfort is always the same
if df['comfort_score'].nunique() < 10:
    issues.append("⚠️ CRITICAL: Comfort score has very few unique values - not enough diversity!")

# Check if actions would make a difference
if df['energy_consumed_kw'].std() < 0.5:
    issues.append("⚠️ WARNING: Energy consumption doesn't vary much - reward signal may be weak!")

# Check data range
if len(df) < 10000:
    issues.append("⚠️ WARNING: Dataset may be too small for effective training (< 10k samples)")

if len(issues) == 0:
    print("✅ No critical issues found!")
else:
    for issue in issues:
        print(issue)

# 9. Training Recommendations
print("\n9. TRAINING RECOMMENDATIONS")
print("-"*40)

if df['comfort_score'].var() < 0.01:
    print("❌ DATASET NOT SUITABLE FOR TRAINING")
    print("   The comfort scores are too uniform. The AI has no way to learn")
    print("   what actions lead to better comfort.")
    print("\n   SOLUTION: You need a dataset with:")
    print("   • Varying comfort scores (0.1 to 0.9 range)")
    print("   • Clear cause-effect relationships")
    print("   • Diverse scenarios (hot/cold, day/night, occupied/unoccupied)")
else:
    print("✅ Dataset appears suitable for basic training")
    
    # Optimal training parameters
    optimal_timesteps = len(df) * 5  # Train for 5 passes through data
    print(f"\n   Recommended training timesteps: {optimal_timesteps:,}")
    print(f"   (Current setting: 50,000 - {'OK' if 50000 >= len(df) else 'TOO LOW'})")
    
    if df['comfort_score'].std() > 0.1:
        print("   • Good comfort variation - AI should learn well")
    else:
        print("   • Low comfort variation - AI may struggle to learn")

# 10. Save diagnostic plots
print("\n10. GENERATING DIAGNOSTIC PLOTS...")
print("-"*40)

fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Plot 1: Temperature over time
axes[0, 0].plot(df.index[:1440], df['room_temperature_c'][:1440])
axes[0, 0].set_title('Temperature - First Day')
axes[0, 0].set_xlabel('Time (minutes)')
axes[0, 0].set_ylabel('Temperature (°C)')

# Plot 2: Comfort score distribution
axes[0, 1].hist(df['comfort_score'], bins=50, edgecolor='black')
axes[0, 1].set_title('Comfort Score Distribution')
axes[0, 1].set_xlabel('Comfort Score')
axes[0, 1].set_ylabel('Frequency')

# Plot 3: Light levels over day
axes[1, 0].plot(df.index[:1440], df['ambient_light_lux'][:1440])
axes[1, 0].set_title('Light Levels - First Day')
axes[1, 0].set_xlabel('Time (minutes)')
axes[1, 0].set_ylabel('Light (lux)')

# Plot 4: Energy consumption
axes[1, 1].hist(df['energy_consumed_kw'], bins=50, edgecolor='black')
axes[1, 1].set_title('Energy Consumption Distribution')
axes[1, 1].set_xlabel('Energy (kW)')
axes[1, 1].set_ylabel('Frequency')

plt.tight_layout()
plt.savefig('dataset_diagnostics.png', dpi=150)
print("✅ Saved diagnostic plots to: dataset_diagnostics.png")

print("\n" + "="*60)
print("VALIDATION COMPLETE")
print("="*60)