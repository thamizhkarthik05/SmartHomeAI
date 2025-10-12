import gymnasium as gym
from gymnasium import spaces
import pandas as pd
import numpy as np
import random

class DynamicSmartHomeEnv(gym.Env):
    """
    Enhanced Smart Home Environment with more realistic variability
    """

    def __init__(self, data_file="SmartHome_Environment_v1.csv", dynamic_mode=True):
        super(DynamicSmartHomeEnv, self).__init__()

        # Load dataset
        self.df = pd.read_csv(data_file)
        self.df["fan_state"] = self.df["fan_state"].apply(lambda x: 1 if str(x).lower() == "on" else 0)
        self.df["user_override_event"] = self.df["user_override_event"].apply(lambda x: 1 if str(x).upper() == "TRUE" else 0)

        self.current_step = 0
        self.dynamic_mode = dynamic_mode
        
        # Dynamic state variables
        self.room_temp_offset = 0
        self.outdoor_temp = 20
        self.occupancy_level = 0  # 0-3 people
        self.activity_level = 0   # 0-2 (sleeping, normal, active)
        self.weather_factor = 1.0  # Weather impact multiplier
        
        # Action and observation spaces (same as original)
        self.action_space = spaces.Discrete(5)
        low = np.array([0, 0, 0, 0, 0, 0, 0], dtype=np.float32)
        high = np.array([40, 40, 2000, 1, 1, 100, 10], dtype=np.float32)
        self.observation_space = spaces.Box(low, high, dtype=np.float32)

    def _apply_dynamic_effects(self, base_obs):
        """Apply realistic dynamic effects to base observations"""
        if not self.dynamic_mode:
            return base_obs
            
        # Get base values
        room_temp = base_obs[0] + self.room_temp_offset
        perceived_temp = base_obs[1]
        ambient_light = base_obs[2]
        comfort = base_obs[3]
        fan_state = base_obs[4]
        light_percent = base_obs[5]
        energy = base_obs[6]
        
        # Time-based effects
        hour = (self.current_step // 60) % 24
        
        # 1. Temperature variations
        # Outdoor temperature affects indoor temp
        seasonal_temp = 20 + 10 * np.sin((self.current_step / (24*60)) * 2 * np.pi / 365)
        daily_temp_cycle = 3 * np.sin((hour - 6) * np.pi / 12)  # Peak at 2 PM
        
        # Occupancy heating
        occupancy_heat = self.occupancy_level * 1.5
        activity_heat = self.activity_level * 1.0
        
        # Weather effects
        weather_temp_impact = random.uniform(-2, 3) * self.weather_factor
        
        room_temp = (seasonal_temp + daily_temp_cycle + occupancy_heat + 
                    activity_heat + weather_temp_impact + self.room_temp_offset)
        room_temp = max(10, min(35, room_temp))  # Clamp to realistic range
        
        # 2. Light variations
        if 6 <= hour <= 18:  # Daytime
            natural_light = 800 * np.sin((hour - 6) * np.pi / 12)  # Peak at noon
        else:  # Nighttime
            natural_light = random.uniform(0, 50)
            
        # Occupancy affects artificial lighting
        if self.occupancy_level > 0:
            if 18 <= hour or hour <= 6:  # Evening/night
                light_percent = min(100, light_percent + 30 + (self.occupancy_level * 20))
            else:  # Day
                light_percent = max(20, light_percent + (self.occupancy_level * 10))
        
        ambient_light = natural_light + (light_percent * 5)  # Artificial light contribution
        
        # 3. Dynamic comfort calculation
        # Comfort depends on temperature deviation, light adequacy, and activity
        temp_comfort = max(0, 1 - abs(room_temp - 22) / 8)
        
        # Light comfort varies by time and activity
        if 6 <= hour <= 22:  # Waking hours
            ideal_light = 400 + (self.activity_level * 200)
        else:  # Sleeping hours
            ideal_light = 50
            
        light_comfort = max(0, 1 - abs(ambient_light - ideal_light) / ideal_light)
        
        # Overall comfort
        comfort = (temp_comfort * 0.6 + light_comfort * 0.4) * max(0.3, 1 - self.occupancy_level * 0.1)
        
        # 4. Dynamic energy calculation
        base_energy = 0.5  # Base consumption
        fan_energy = fan_state * (0.3 + abs(room_temp - 22) * 0.1)
        light_energy = (light_percent / 100) * 0.8
        hvac_energy = abs(room_temp - 22) * 0.2  # HVAC working harder
        
        energy = base_energy + fan_energy + light_energy + hvac_energy
        
        # 5. Add some random noise for realism
        room_temp += random.uniform(-0.5, 0.5)
        ambient_light += random.uniform(-20, 20)
        comfort = max(0, min(1, comfort + random.uniform(-0.05, 0.05)))
        
        return np.array([
            room_temp,
            perceived_temp + random.uniform(-0.3, 0.3),
            max(0, ambient_light),
            comfort,
            fan_state,
            max(0, min(100, light_percent)),
            max(0, energy)
        ], dtype=np.float32)

    def _update_dynamic_state(self, action):
        """Update dynamic environmental factors"""
        hour = (self.current_step // 60) % 24
        
        # Update occupancy based on time of day
        if 7 <= hour <= 9 or 17 <= hour <= 22:  # Morning/evening - people home
            self.occupancy_level = random.choice([1, 2, 2, 3])
        elif 9 <= hour <= 17:  # Work hours - lower occupancy
            self.occupancy_level = random.choice([0, 0, 1, 1])
        else:  # Night/early morning - sleeping
            self.occupancy_level = random.choice([1, 2, 2])
            
        # Update activity level
        if 22 <= hour or hour <= 6:  # Sleep time
            self.activity_level = 0
        elif 6 <= hour <= 9 or 17 <= hour <= 21:  # Active times
            self.activity_level = random.choice([1, 2])
        else:  # Normal day
            self.activity_level = 1
            
        # Weather changes (simulate weather patterns)
        if random.random() < 0.1:  # 10% chance of weather change
            self.weather_factor = random.uniform(0.5, 2.0)
            
        # Apply action effects to room temperature
        if action == 1:  # Turn fan on
            self.room_temp_offset -= 1.0
        elif action == 2:  # Turn fan off
            self.room_temp_offset = max(-3, self.room_temp_offset + 0.5)
            
        # Temperature drift towards outdoor temp
        self.room_temp_offset *= 0.95  # Gradual return to baseline

    def _get_obs(self):
        if self.current_step >= len(self.df):
            return np.zeros(self.observation_space.shape, dtype=np.float32)
            
        # Get base observation from dataset
        row = self.df.iloc[self.current_step]
        base_obs = np.array([
            row["room_temperature_c"],
            row["perceived_temperature_c"],
            row["ambient_light_lux"],
            row["comfort_score"],
            row["fan_state"],
            row["light_state_percent"],
            row["energy_consumed_kw"]
        ], dtype=np.float32)
        
        # Apply dynamic effects
        return self._apply_dynamic_effects(base_obs)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = options.get('start_step', 0) if options else 0
        
        # Reset dynamic state
        self.room_temp_offset = 0
        self.occupancy_level = 1
        self.activity_level = 1
        self.weather_factor = 1.0
        
        return self._get_obs(), {}

    def step(self, action):
        # Update dynamic environmental state
        self._update_dynamic_state(action)
        
        # Get current observation
        obs = self._get_obs()
        
        # Enhanced reward function
        reward = 0
        
        # Comfort reward (main goal)
        comfort = obs[3]
        reward += comfort * 15  # Higher weight for comfort
        
        # Energy efficiency
        energy = obs[6]
        reward -= energy * 1.5
        
        # Temperature optimization
        temp = obs[0]
        if 20 <= temp <= 24:  # Ideal range
            reward += 5
        else:
            reward -= abs(temp - 22) * 0.5
            
        # Light optimization  
        hour = (self.current_step // 60) % 24
        light_level = obs[2]
        if 6 <= hour <= 22:  # Waking hours
            if light_level >= 300:
                reward += 2
        else:  # Sleeping hours
            if light_level <= 100:
                reward += 3
                
        # Action efficiency (penalize unnecessary actions)
        if action != 0:
            reward -= 1
            
        # User override penalty (simulated)
        if random.random() < 0.05:  # 5% chance of user override
            reward -= 15
            
        # Move to next step
        self.current_step += 1
        terminated = self.current_step >= len(self.df) - 1

        if terminated:
            obs = np.zeros(self.observation_space.shape, dtype=np.float32)

        info = {
            'occupancy': self.occupancy_level,
            'activity': self.activity_level,
            'weather_factor': self.weather_factor,
            'hour': (self.current_step // 60) % 24
        }

        return obs, reward, terminated, False, info

    def render(self, mode="human"):
        obs = self._get_obs()
        hour = (self.current_step // 60) % 24
        minute = self.current_step % 60
        
        print(f"🕐 {hour:02d}:{minute:02d} | "
              f"🌡️ {obs[0]:.1f}°C | "
              f"💡 {obs[2]:.0f}lux | "
              f"😊 {obs[3]:.2f} | "
              f"👥 {self.occupancy_level} people | "
              f"🏃 Activity: {self.activity_level}")