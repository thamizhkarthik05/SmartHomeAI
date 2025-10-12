import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

print("🏠 Generating Realistic Smart Home Dataset")
print("=" * 60)

# Configuration
DAYS = 30
MINUTES_PER_DAY = 1440
TOTAL_MINUTES = DAYS * MINUTES_PER_DAY

# Climate: Hot region (25-35°C typical)
BASE_OUTDOOR_TEMP = 28  # Average outdoor temperature

print(f"📅 Duration: {DAYS} days")
print(f"📊 Total data points: {TOTAL_MINUTES:,}")
print(f"🌡️ Climate: Hot (25-35°C outdoor)")
print(f"👥 Occupants: Multiple (family)")
print()

# Initialize data storage
data = {
    'timestamp': [],
    'persona_id': [],
    'is_occupied': [],
    'num_occupants': [],
    'room_temperature_c': [],
    'perceived_temperature_c': [],
    'ambient_light_lux': [],
    'comfort_score': [],
    'fan_state': [],
    'light_state_percent': [],
    'energy_consumed_kw': [],
    'user_override_event': []
}

# State variables
current_temp = 26.0  # Start at room temperature
fan_on = False
light_level = 0
outdoor_temp = BASE_OUTDOOR_TEMP

# Helper functions
def get_outdoor_temperature(day, hour, minute):
    """Calculate outdoor temperature with daily and seasonal variations"""
    # Daily cycle: cooler at night (4 AM), hottest at 2 PM
    time_of_day = hour + minute / 60
    daily_variation = 5 * np.sin((time_of_day - 6) * np.pi / 12)  # Peak at 2 PM
    
    # Seasonal variation over 30 days (simulate summer)
    seasonal_variation = 2 * np.sin(day * np.pi / 15)
    
    # Random weather fluctuations
    weather_noise = np.random.normal(0, 1)
    
    base_temp = BASE_OUTDOOR_TEMP + daily_variation + seasonal_variation + weather_noise
    return max(20, min(40, base_temp))  # Clamp between 20-40°C

def get_occupancy_pattern(day, hour, minute):
    """Determine occupancy for a family (returns number of occupants 0-4)"""
    is_weekend = day % 7 >= 5  # Saturday, Sunday
    
    if is_weekend:
        # Weekend: More people home
        if 0 <= hour < 7:  # Late night/early morning
            return random.choice([2, 3, 4])  # Sleeping
        elif 7 <= hour < 10:  # Morning
            return random.choice([2, 3, 4])  # Breakfast time
        elif 10 <= hour < 18:  # Day
            return random.choice([1, 2, 3, 4])  # Various activities
        elif 18 <= hour < 23:  # Evening
            return random.choice([3, 4])  # Family together
        else:  # Night
            return random.choice([2, 3, 4])  # Sleeping
    else:
        # Weekday: Work/school patterns
        if 0 <= hour < 6:  # Late night
            return random.choice([2, 3])  # Sleeping
        elif 6 <= hour < 9:  # Morning rush
            return random.choice([2, 3, 4])  # Getting ready
        elif 9 <= hour < 15:  # Day (work/school)
            return random.choice([0, 1])  # Mostly empty
        elif 15 <= hour < 17:  # Afternoon (kids back)
            return random.choice([1, 2])  # Some people home
        elif 17 <= hour < 22:  # Evening (family time)
            return random.choice([3, 4])  # Most/all home
        elif 22 <= hour < 24:  # Night
            return random.choice([2, 3, 4])  # Going to bed
        else:
            return random.choice([2, 3])

def get_activity_level(num_occupants, hour):
    """Get activity level based on occupants and time"""
    if num_occupants == 0:
        return 0  # No activity
    
    if 6 <= hour < 9 or 17 <= hour < 21:  # Active periods
        return min(1.0, num_occupants * 0.3)
    elif 9 <= hour < 17:  # Moderate day activity
        return min(0.8, num_occupants * 0.25)
    else:  # Low activity (sleeping)
        return min(0.3, num_occupants * 0.1)

def calculate_natural_light(hour, minute):
    """Calculate natural sunlight based on time of day"""
    time_of_day = hour + minute / 60
    
    if 6 <= time_of_day <= 18:  # Daylight hours
        # Peak at noon (12:00)
        sun_angle = np.sin((time_of_day - 6) * np.pi / 12)
        natural_light = 800 * sun_angle  # Max 800 lux natural light
        # Add some clouds variation
        cloud_factor = random.uniform(0.7, 1.0)
        return natural_light * cloud_factor
    else:
        return random.uniform(0, 20)  # Minimal ambient light at night

def calculate_ideal_light(num_occupants, hour, activity_level):
    """Calculate ideal artificial lighting based on occupancy and activity"""
    if num_occupants == 0:
        return 0  # No one home
    
    if 6 <= hour < 9:  # Morning
        return 400 + (num_occupants * 50)
    elif 9 <= hour < 17:  # Day
        return 300 + (num_occupants * 40)  # Less artificial (natural light)
    elif 17 <= hour < 22:  # Evening
        return 500 + (num_occupants * 60)
    elif 22 <= hour < 24:  # Late evening
        return 150 + (num_occupants * 30)
    else:  # Night
        return 20 if num_occupants > 0 else 0

def calculate_comfort(temp, light, num_occupants, hour, activity_level):
    """Calculate comfort score based on multiple factors"""
    if num_occupants == 0:
        return 0.0  # No one to be comfortable
    
    # Ideal temperature depends on activity and time
    if 22 <= hour or hour < 6:  # Sleeping
        ideal_temp = 22  # Cooler for sleeping
    elif activity_level > 0.7:  # High activity
        ideal_temp = 23
    else:  # Normal activity
        ideal_temp = 24
    
    # Temperature comfort (most important for hot climate)
    temp_deviation = abs(temp - ideal_temp)
    if temp_deviation <= 1:
        temp_comfort = 1.0
    elif temp_deviation <= 3:
        temp_comfort = 0.8 - (temp_deviation - 1) * 0.15
    else:
        temp_comfort = max(0.0, 0.5 - (temp_deviation - 3) * 0.1)
    
    # Lighting comfort
    ideal_light_level = calculate_ideal_light(num_occupants, hour, activity_level)
    natural_light = calculate_natural_light(hour, 0)
    total_light = light + natural_light
    
    light_deviation = abs(total_light - ideal_light_level)
    if light_deviation <= 100:
        light_comfort = 1.0
    elif light_deviation <= 300:
        light_comfort = 0.8 - (light_deviation - 100) * 0.002
    else:
        light_comfort = max(0.0, 0.4 - (light_deviation - 300) * 0.001)
    
    # Combined comfort (temperature weighted more in hot climate)
    comfort = temp_comfort * 0.65 + light_comfort * 0.35
    
    # Adjust for number of occupants (more people = more critical)
    occupancy_weight = min(1.0, 0.5 + (num_occupants * 0.15))
    
    return min(1.0, comfort * occupancy_weight)

def simulate_user_override(comfort, num_occupants, last_override_time, current_time):
    """Determine if user would manually override the system"""
    if num_occupants == 0:
        return False
    
    # Don't override too frequently (at least 30 minutes apart)
    if current_time - last_override_time < 30:
        return False
    
    # Probability increases as comfort decreases
    if comfort < 0.3:
        return random.random() < 0.15  # 15% chance if very uncomfortable
    elif comfort < 0.5:
        return random.random() < 0.05  # 5% chance if uncomfortable
    elif comfort < 0.6:
        return random.random() < 0.01  # 1% chance if slightly uncomfortable
    
    return False

# Generation loop
print("⏳ Generating data...")
last_override_time = -100  # Track last override

for day in range(DAYS):
    for hour in range(24):
        for minute in range(60):
            current_time = day * 1440 + hour * 60 + minute
            
            # Progress indicator
            if current_time % 5000 == 0:
                progress = (current_time / TOTAL_MINUTES) * 100
                print(f"   Progress: {progress:.1f}% (Day {day+1}/{DAYS})")
            
            # Time
            timestamp = datetime(2025, 1, 1) + timedelta(minutes=current_time)
            
            # Occupancy
            num_occupants = get_occupancy_pattern(day, hour, minute)
            is_occupied = num_occupants > 0
            activity_level = get_activity_level(num_occupants, hour)
            
            # Outdoor temperature
            outdoor_temp = get_outdoor_temperature(day, hour, minute)
            
            # Temperature dynamics
            # 1. Natural drift towards outdoor temp
            temp_drift = (outdoor_temp - current_temp) * 0.02
            
            # 2. Occupancy heating (people generate heat)
            occupancy_heat = num_occupants * 0.01
            
            # 3. Fan cooling effect
            if fan_on:
                fan_cooling = -0.08  # Fan cools room
            else:
                fan_cooling = 0
            
            # 4. Light heating (minimal)
            light_heating = (light_level / 100) * 0.005
            
            # Update temperature
            current_temp += temp_drift + occupancy_heat + fan_cooling + light_heating
            current_temp = max(18, min(40, current_temp))  # Clamp
            
            # Perceived temperature (with humidity factor in hot climate)
            humidity_factor = random.uniform(0.5, 1.5)
            perceived_temp = current_temp + humidity_factor
            
            # Natural light
            natural_light = calculate_natural_light(hour, minute)
            
            # Total ambient light
            artificial_light = light_level * 8  # Convert percentage to lux
            ambient_light = natural_light + artificial_light
            
            # Calculate comfort
            comfort = calculate_comfort(current_temp, ambient_light, num_occupants, 
                                       hour, activity_level)
            
            # User override decision
            user_override = simulate_user_override(comfort, num_occupants, 
                                                   last_override_time, current_time)
            
            if user_override:
                last_override_time = current_time
                # User takes corrective action
                if current_temp > 25 and not fan_on:
                    fan_on = True  # Turn on fan if hot
                elif current_temp < 22 and fan_on:
                    fan_on = False  # Turn off fan if cool enough
                
                # Adjust lights
                ideal_light = calculate_ideal_light(num_occupants, hour, activity_level)
                if ambient_light < ideal_light - 200:
                    light_level = min(100, light_level + 30)
                elif ambient_light > ideal_light + 200:
                    light_level = max(0, light_level - 30)
            
            # Energy consumption
            fan_energy = 1.2 if fan_on else 0.0
            light_energy = (light_level / 100) * 0.6
            base_energy = 0.3  # Base household consumption
            total_energy = fan_energy + light_energy + base_energy
            
            # Store data
            data['timestamp'].append(timestamp.strftime('%d/%m/%Y %H:%M'))
            data['persona_id'].append('family')
            data['is_occupied'].append(is_occupied)
            data['num_occupants'].append(num_occupants)
            data['room_temperature_c'].append(round(current_temp, 2))
            data['perceived_temperature_c'].append(round(perceived_temp, 2))
            data['ambient_light_lux'].append(round(ambient_light, 0))
            data['comfort_score'].append(round(comfort, 3))
            data['fan_state'].append('on' if fan_on else 'off')
            data['light_state_percent'].append(round(light_level, 0))
            data['energy_consumed_kw'].append(round(total_energy, 3))
            data['user_override_event'].append(user_override)

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
output_file = 'SmartHome_Realistic_Dataset.csv'
df.to_csv(output_file, index=False)

print(f"\n✅ Dataset generated successfully!")
print(f"📁 Saved to: {output_file}")
print()

# Generate statistics
print("=" * 60)
print("DATASET STATISTICS")
print("=" * 60)

print(f"\n📊 Basic Info:")
print(f"   Total records: {len(df):,}")
print(f"   Duration: {DAYS} days")
print(f"   Interval: 1 minute")

print(f"\n🌡️ Temperature:")
print(f"   Range: {df['room_temperature_c'].min():.1f}°C to {df['room_temperature_c'].max():.1f}°C")
print(f"   Mean: {df['room_temperature_c'].mean():.1f}°C")
print(f"   Std Dev: {df['room_temperature_c'].std():.2f}")
print(f"   Variance: {df['room_temperature_c'].var():.2f}")

print(f"\n😊 Comfort Score:")
print(f"   Range: {df['comfort_score'].min():.3f} to {df['comfort_score'].max():.3f}")
print(f"   Mean: {df['comfort_score'].mean():.3f}")
print(f"   Std Dev: {df['comfort_score'].std():.3f}")
print(f"   Variance: {df['comfort_score'].var():.4f}")
print(f"   Above 0.7: {(df['comfort_score'] >= 0.7).sum() / len(df) * 100:.1f}%")
print(f"   Above 0.5: {(df['comfort_score'] >= 0.5).sum() / len(df) * 100:.1f}%")

print(f"\n💡 Lighting:")
print(f"   Range: {df['ambient_light_lux'].min():.0f} to {df['ambient_light_lux'].max():.0f} lux")
print(f"   Mean: {df['ambient_light_lux'].mean():.0f} lux")
print(f"   Variance: {df['ambient_light_lux'].var():.0f}")

print(f"\n⚡ Energy:")
print(f"   Range: {df['energy_consumed_kw'].min():.2f} to {df['energy_consumed_kw'].max():.2f} kW")
print(f"   Mean: {df['energy_consumed_kw'].mean():.2f} kW")
print(f"   Std Dev: {df['energy_consumed_kw'].std():.2f}")

print(f"\n👥 Occupancy:")
print(f"   Occupied: {(df['is_occupied'] == True).sum() / len(df) * 100:.1f}%")
print(f"   Unoccupied: {(df['is_occupied'] == False).sum() / len(df) * 100:.1f}%")
print(f"   Avg occupants when occupied: {df[df['is_occupied'] == True]['num_occupants'].mean():.1f}")

print(f"\n🔧 User Overrides:")
print(f"   Total: {df['user_override_event'].sum()} events")
print(f"   Rate: {df['user_override_event'].sum() / len(df) * 100:.2f}%")

print(f"\n🌀 Fan Usage:")
print(f"   On: {(df['fan_state'] == 'on').sum() / len(df) * 100:.1f}%")
print(f"   Off: {(df['fan_state'] == 'off').sum() / len(df) * 100:.1f}%")

# Validation checks
print("\n" + "=" * 60)
print("VALIDATION FOR ML TRAINING")
print("=" * 60)

checks = []
if df['comfort_score'].var() > 0.05:
    checks.append("✅ Comfort variance: GOOD (> 0.05)")
else:
    checks.append("❌ Comfort variance: TOO LOW")

if df['comfort_score'].std() > 0.15:
    checks.append("✅ Comfort std dev: GOOD (> 0.15)")
else:
    checks.append("⚠️ Comfort std dev: ACCEPTABLE")

if df['room_temperature_c'].var() > 5.0:
    checks.append("✅ Temperature variance: GOOD (> 5.0)")
else:
    checks.append("⚠️ Temperature variance: LOW")

if df['energy_consumed_kw'].std() > 0.3:
    checks.append("✅ Energy variance: GOOD (> 0.3)")
else:
    checks.append("⚠️ Energy variance: LOW")

if df['user_override_event'].sum() > 100:
    checks.append("✅ Sufficient override events for learning")
else:
    checks.append("⚠️ Few override events")

if len(df) >= 30000:
    checks.append("✅ Dataset size: SUFFICIENT (≥ 30k)")
else:
    checks.append("⚠️ Dataset size: SMALL")

for check in checks:
    print(check)

# Overall verdict
passed = sum(1 for c in checks if c.startswith("✅"))
total = len(checks)

print(f"\n📊 Overall: {passed}/{total} checks passed")

if passed >= 4:
    print("🎉 ✅ DATASET IS SUITABLE FOR TRAINING!")
    print("   This dataset has sufficient variation and patterns for RL learning")
else:
    print("⚠️ Dataset may need improvements")

print("\n" + "=" * 60)
print("🚀 NEXT STEPS:")
print("=" * 60)
print("1. Review the dataset: explore_data.py")
print("2. Update train.py to use: SmartHome_Realistic_Dataset.csv")
print("3. Train the model: python train.py")
print("4. Test the trained model: python test_agent.py")
print("5. Validate performance: python ai_validator.py")
print("=" * 60)