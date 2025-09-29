import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset you generated
df = pd.read_csv('SmartHome_Environment_v1.csv')

# Convert timestamp to a datetime object for plotting
df['timestamp'] = pd.to_datetime(df['timestamp'], dayfirst=True)

print("--- Dataset Information ---")
print(df.info())
print("\n--- First 5 Rows ---")
print(df.head())

# --- Create Visualizations ---

# Set a style for the plots
sns.set_style("whitegrid")

# 1. Plot temperature and light over the first week to see the daily cycles
print("\nGenerating plot for first week's environment...")
plt.figure(figsize=(15, 7))
plt.plot(df['timestamp'][:10080], df['room_temperature_c'][:10080], label='Room Temperature (°C)', color='red')
plt.title('Environmental Conditions Over One Week')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.twinx() # Create a second y-axis for light
plt.plot(df['timestamp'][:10080], df['ambient_light_lux'][:10080], label='Ambient Light (lux)', color='orange', alpha=0.6)
plt.ylabel('Light (lux)')
plt.legend(loc='upper right')
plt.savefig('weekly_environment.png') # Save the plot as an image file
plt.close()
print("Saved 'weekly_environment.png'")

# 2. Plot where user overrides happen
print("Generating plot for user overrides...")
override_events = df[df['user_override_event'] == True]
plt.figure(figsize=(12, 6))
sns.histplot(override_events['room_temperature_c'], bins=20, kde=True)
plt.title('At What Temperatures Do Users Override the System?')
plt.xlabel('Room Temperature (°C) when Override Occurred')
plt.ylabel('Number of Overrides')
plt.savefig('override_temperatures.png')
plt.close()
print("Saved 'override_temperatures.png'")

print("\nExploration complete. Check the saved .png files for plots.")





