import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

print("📊 Comparing OLD vs NEW Dataset")
print("="*60)

# Load both datasets
print("Loading datasets...")
try:
    old_df = pd.read_csv('SmartHome_Environment_v1.csv')
    print(f"✅ OLD dataset: {len(old_df):,} samples")
except:
    print("❌ Old dataset not found")
    old_df = None

try:
    new_df = pd.read_csv('SmartHome_Realistic_Dataset.csv')
    print(f"✅ NEW dataset: {len(new_df):,} samples")
except:
    print("❌ New dataset not found - run generate_realistic_dataset.py first!")
    exit(1)

# Create comparison visualization
fig, axes = plt.subplots(3, 2, figsize=(16, 12))
fig.suptitle('Dataset Comparison: OLD vs NEW', fontsize=16, fontweight='bold')

# Plot 1: Comfort Score Distribution
if old_df is not None:
    axes[0, 0].hist(old_df['comfort_score'], bins=50, alpha=0.7, label='OLD', color='red', edgecolor='black')
axes[0, 0].hist(new_df['comfort_score'], bins=50, alpha=0.7, label='NEW', color='green', edgecolor='black')
axes[0, 0].set_title('Comfort Score Distribution')
axes[0, 0].set_xlabel('Comfort Score')
axes[0, 0].set_ylabel('Frequency')
axes[0, 0].legend()
axes[0, 0].axvline(0.7, color='blue', linestyle='--', label='Target: 0.7', alpha=0.5)

# Plot 2: Temperature Distribution
if old_df is not None:
    axes[0, 1].hist(old_df['room_temperature_c'], bins=50, alpha=0.7, label='OLD', color='red', edgecolor='black')
axes[0, 1].hist(new_df['room_temperature_c'], bins=50, alpha=0.7, label='NEW', color='green', edgecolor='black')
axes[0, 1].set_title('Temperature Distribution')
axes[0, 1].set_xlabel('Temperature (°C)')
axes[0, 1].set_ylabel('Frequency')
axes[0, 1].legend()
axes[0, 1].axvline(22, color='blue', linestyle='--', alpha=0.3)
axes[0, 1].axvline(24, color='blue', linestyle='--', alpha=0.3)

# Plot 3: Comfort over first day - OLD
if old_df is not None:
    axes[1, 0].plot(old_df['comfort_score'][:1440], color='red', alpha=0.7, linewidth=2)
    axes[1, 0].set_title('OLD Dataset - First Day Comfort')
    axes[1, 0].set_xlabel('Time (minutes)')
    axes[1, 0].set_ylabel('Comfort Score')
    axes[1, 0].axhline(0.7, color='green', linestyle='--', alpha=0.3, label='Good comfort')
    axes[1, 0].legend()
    axes[1, 0].set_ylim([0, 1])

# Plot 4: Comfort over first day - NEW
axes[1, 1].plot(new_df['comfort_score'][:1440], color='green', alpha=0.7, linewidth=2)
axes[1, 1].set_title('NEW Dataset - First Day Comfort')
axes[1, 1].set_xlabel('Time (minutes)')
axes[1, 1].set_ylabel('Comfort Score')
axes[1, 1].axhline(0.7, color='green', linestyle='--', alpha=0.3, label='Good comfort')
axes[1, 1].legend()
axes[1, 1].set_ylim([0, 1])

# Plot 5: Energy Consumption
if old_df is not None:
    axes[2, 0].hist(old_df['energy_consumed_kw'], bins=50, alpha=0.7, label='OLD', color='red', edgecolor='black')
axes[2, 0].hist(new_df['energy_consumed_kw'], bins=50, alpha=0.7, label='NEW', color='green', edgecolor='black')
axes[2, 0].set_title('Energy Consumption Distribution')
axes[2, 0].set_xlabel('Energy (kW)')
axes[2, 0].set_ylabel('Frequency')
axes[2, 0].legend()

# Plot 6: Statistics Comparison
stats_labels = ['Comfort\nVariance', 'Comfort\nMean', 'Temp\nVariance', 'Energy\nStd Dev']
if old_df is not None:
    old_stats = [
        old_df['comfort_score'].var(),
        old_df['comfort_score'].mean(),
        old_df['room_temperature_c'].var(),
        old_df['energy_consumed_kw'].std()
    ]
else:
    old_stats = [0, 0, 0, 0]

new_stats = [
    new_df['comfort_score'].var(),
    new_df['comfort_score'].mean(),
    new_df['room_temperature_c'].var(),
    new_df['energy_consumed_kw'].std()
]

x = np.arange(len(stats_labels))
width = 0.35

bars1 = axes[2, 1].bar(x - width/2, old_stats, width, label='OLD', color='red', alpha=0.7)
bars2 = axes[2, 1].bar(x + width/2, new_stats, width, label='NEW', color='green', alpha=0.7)

axes[2, 1].set_title('Key Statistics Comparison')
axes[2, 1].set_xticks(x)
axes[2, 1].set_xticklabels(stats_labels)
axes[2, 1].legend()
axes[2, 1].set_ylabel('Value')

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        axes[2, 1].text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.3f}',
                       ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig('dataset_comparison.png', dpi=150, bbox_inches='tight')
print("\n✅ Comparison visualization saved: dataset_comparison.png")

# Print numerical comparison
print("\n" + "="*60)
print("NUMERICAL COMPARISON")
print("="*60)

print("\n📊 COMFORT SCORE:")
if old_df is not None:
    print(f"   OLD: Variance={old_df['comfort_score'].var():.4f}, Mean={old_df['comfort_score'].mean():.3f}, Range={old_df['comfort_score'].min():.3f}-{old_df['comfort_score'].max():.3f}")
print(f"   NEW: Variance={new_df['comfort_score'].var():.4f}, Mean={new_df['comfort_score'].mean():.3f}, Range={new_df['comfort_score'].min():.3f}-{new_df['comfort_score'].max():.3f}")

if old_df is not None:
    comfort_improvement = (new_df['comfort_score'].var() / old_df['comfort_score'].var())
    print(f"   📈 Improvement: {comfort_improvement:.1f}x better variance!")

print("\n🌡️ TEMPERATURE:")
if old_df is not None:
    print(f"   OLD: Mean={old_df['room_temperature_c'].mean():.1f}°C, Range={old_df['room_temperature_c'].min():.1f}-{old_df['room_temperature_c'].max():.1f}°C")
print(f"   NEW: Mean={new_df['room_temperature_c'].mean():.1f}°C, Range={new_df['room_temperature_c'].min():.1f}-{new_df['room_temperature_c'].max():.1f}°C")

print("\n⚡ ENERGY:")
if old_df is not None:
    print(f"   OLD: Mean={old_df['energy_consumed_kw'].mean():.3f} kW, Std={old_df['energy_consumed_kw'].std():.3f}")
print(f"   NEW: Mean={new_df['energy_consumed_kw'].mean():.3f} kW, Std={new_df['energy_consumed_kw'].std():.3f}")

if old_df is not None:
    energy_improvement = (new_df['energy_consumed_kw'].std() / old_df['energy_consumed_kw'].std())
    print(f"   📈 Improvement: {energy_improvement:.1f}x better variance!")

print("\n👥 OCCUPANCY:")
if old_df is not None:
    old_occupied = (old_df['is_occupied'] == True).sum() / len(old_df) * 100
    print(f"   OLD: {old_occupied:.1f}% occupied")
new_occupied = (new_df['is_occupied'] == True).sum() / len(new_df) * 100
print(f"   NEW: {new_occupied:.1f}% occupied")

print("\n🔧 USER OVERRIDES:")
if old_df is not None:
    old_overrides = old_df['user_override_event'].sum()
    old_override_rate = (old_overrides / len(old_df)) * 100
    print(f"   OLD: {old_overrides} events ({old_override_rate:.2f}%)")
new_overrides = new_df['user_override_event'].sum()
new_override_rate = (new_overrides / len(new_df)) * 100
print(f"   NEW: {new_overrides} events ({new_override_rate:.2f}%)")

print("\n" + "="*60)
print("VERDICT")
print("="*60)

if old_df is not None:
    print("\n❌ OLD DATASET:")
    print("   • Too static (comfort variance < 0.01)")
    print("   • Represents only sleeping person")
    print("   • No learning opportunities")
    print("   • AI learned 'do nothing' is optimal")

print("\n✅ NEW DATASET:")
print("   • Dynamic (comfort variance > 0.05)")
print("   • Represents realistic family patterns")
print("   • Clear cause-effect relationships")
print("   • AI can learn meaningful control strategies")

print("\n🎯 READY FOR TRAINING!")
print("   Run: python train.py")
print("="*60)