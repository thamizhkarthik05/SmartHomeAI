"""
Realistic Dynamic Smart Home Environment - No CSV needed
Generates truly realistic, non-repetitive inputs with learned user preferences
"""
import numpy as np
import gymnasium as gym
from gymnasium import spaces

class RealisticSmartHomeEnv(gym.Env):
    """
    Fully dynamic smart home with:
    - No CSV dependency
    - Realistic time-based patterns
    - Weather simulation
    - User comfort preferences (simulated learning)
    - Random but realistic variations
    """
    
    def __init__(self):
        super(RealisticSmartHomeEnv, self).__init__()
        
        # Action space
        self.action_space = spaces.Discrete(5)
        
        # Observation space
        self.observation_space = spaces.Box(
            low=np.array([10.0, 20.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
            high=np.array([40.0, 100.0, 24.0, 1.0, 1.0, 100.0, 10.0]),
            dtype=np.float32
        )
        
        # USER COMFORT PREFERENCES (This is the key!)
        # These simulate what a real user would want
        self.user_preferences = self._generate_user_preferences()
        
        # Current state
        self.current_temp = 22.0
        self.current_humidity = 50.0
        self.current_time = 8.0
        self.hvac_on = False
        self.lighting = 50.0
        self.energy_usage = 0.0
        
        # External factors
        self.weather = 'sunny'
        self.outside_temp = 25.0
        self.occupancy = True
        self.season = 'spring'
        
        self.step_count = 0
        self.day_count = 0
        
    def _generate_user_preferences(self):
        """
        Generate realistic user comfort preferences
        This simulates a learned user profile
        """
        return {
            # Temperature preferences
            'preferred_temp': np.random.uniform(20, 24),  # Each user likes different temp
            'temp_tolerance': np.random.uniform(1.5, 3.0),  # Some are more sensitive
            
            # Humidity preferences  
            'preferred_humidity': np.random.uniform(40, 60),
            'humidity_tolerance': 15.0,
            
            # Lighting preferences (changes with time)
            'light_preference_morning': np.random.uniform(60, 80),
            'light_preference_day': np.random.uniform(70, 95),
            'light_preference_evening': np.random.uniform(50, 70),
            'light_preference_night': np.random.uniform(10, 30),
            
            # Energy consciousness (0=don't care, 1=very conscious)
            'energy_conscious': np.random.uniform(0.3, 0.8),
            
            # Activity patterns
            'wake_time': np.random.uniform(6, 8),
            'sleep_time': np.random.uniform(22, 24),
            'work_start': 9.0,
            'work_end': 17.0
        }
    
    def _get_weather_temp_effect(self):
        """Weather affects indoor temperature"""
        effects = {
            'sunny': 3.0,
            'hot_day': 5.0,
            'cloudy': 0.0,
            'rainy': -2.0,
            'cold': -4.0
        }
        return effects.get(self.weather, 0.0)
    
    def _update_weather(self):
        """Change weather realistically"""
        if self.step_count % 48 == 0:  # Change every ~12 hours
            # Seasonal weather patterns
            if self.season == 'summer':
                self.weather = np.random.choice(
                    ['sunny', 'hot_day', 'cloudy'], 
                    p=[0.5, 0.3, 0.2]
                )
                self.outside_temp = np.random.uniform(25, 38)
            elif self.season == 'winter':
                self.weather = np.random.choice(
                    ['cloudy', 'rainy', 'cold'],
                    p=[0.4, 0.3, 0.3]
                )
                self.outside_temp = np.random.uniform(5, 18)
            elif self.season == 'spring':
                self.weather = np.random.choice(
                    ['sunny', 'cloudy', 'rainy'],
                    p=[0.4, 0.4, 0.2]
                )
                self.outside_temp = np.random.uniform(15, 28)
            else:  # fall
                self.weather = np.random.choice(
                    ['sunny', 'cloudy', 'rainy', 'cold'],
                    p=[0.3, 0.3, 0.2, 0.2]
                )
                self.outside_temp = np.random.uniform(10, 25)
    
    def _update_occupancy(self):
        """Realistic occupancy based on time and user patterns"""
        hour = self.current_time
        prefs = self.user_preferences
        
        # Sleeping
        if hour < prefs['wake_time'] or hour >= prefs['sleep_time']:
            self.occupancy = True  # Home, sleeping
        # Work hours
        elif prefs['work_start'] <= hour < prefs['work_end']:
            self.occupancy = np.random.random() > 0.8  # 20% chance home (WFH, sick, etc)
        # Morning routine
        elif prefs['wake_time'] <= hour < prefs['work_start']:
            self.occupancy = True
        # Evening
        elif prefs['work_end'] <= hour < prefs['sleep_time']:
            self.occupancy = True
        else:
            self.occupancy = np.random.random() > 0.3
    
    def _calculate_comfort(self):
        """
        Calculate comfort based on USER PREFERENCES
        This is key - comfort is subjective to each user!
        """
        if not self.occupancy:
            return 0.6  # Neutral when away
        
        prefs = self.user_preferences
        
        # Temperature comfort
        temp_diff = abs(self.current_temp - prefs['preferred_temp'])
        temp_comfort = max(0, 1 - (temp_diff / prefs['temp_tolerance']))
        
        # Humidity comfort  
        humidity_diff = abs(self.current_humidity - prefs['preferred_humidity'])
        humidity_comfort = max(0, 1 - (humidity_diff / prefs['humidity_tolerance']))
        
        # Lighting comfort (time-dependent)
        hour = self.current_time
        if hour < 6:
            preferred_light = prefs['light_preference_night']
        elif 6 <= hour < 9:
            preferred_light = prefs['light_preference_morning']
        elif 9 <= hour < 18:
            preferred_light = prefs['light_preference_day']
        elif 18 <= hour < 22:
            preferred_light = prefs['light_preference_evening']
        else:
            preferred_light = prefs['light_preference_night']
        
        light_diff = abs(self.lighting - preferred_light)
        light_comfort = max(0, 1 - (light_diff / 50.0))
        
        # Weighted combination
        comfort = (
            temp_comfort * 0.5 +      # Temperature is most important
            humidity_comfort * 0.3 +   # Humidity matters
            light_comfort * 0.2        # Lighting affects mood
        )
        
        return np.clip(comfort, 0, 1)
    
    def _update_temperature(self):
        """Update temperature with realistic physics"""
        # Outside temperature influence
        outside_influence = (self.outside_temp - self.current_temp) * 0.03
        
        # Time-based natural variation (warmer during day)
        hour_angle = (self.current_time - 6) * np.pi / 12
        daily_variation = 2.0 * np.sin(hour_angle) * 0.05
        
        # HVAC effect
        hvac_effect = 0.0
        if self.hvac_on:
            target = self.user_preferences['preferred_temp']
            if self.current_temp > target:
                hvac_effect = -0.6  # Cooling
            else:
                hvac_effect = 0.6   # Heating
        
        # Random fluctuations
        noise = np.random.normal(0, 0.15)
        
        # Apply all effects
        self.current_temp += outside_influence + daily_variation + hvac_effect + noise
        self.current_temp = np.clip(self.current_temp, 12.0, 38.0)
    
    def _update_humidity(self):
        """Update humidity based on weather"""
        # Weather effects
        target_humidity = {
            'rainy': 75.0,
            'cloudy': 60.0,
            'sunny': 45.0,
            'hot_day': 35.0,
            'cold': 40.0
        }.get(self.weather, 50.0)
        
        # Gradual change
        change = (target_humidity - self.current_humidity) * 0.08
        change += np.random.normal(0, 0.8)
        
        self.current_humidity += change
        self.current_humidity = np.clip(self.current_humidity, 25.0, 85.0)
    
    def _calculate_energy(self):
        """Calculate realistic energy usage"""
        energy = 0.3  # Base load
        
        # HVAC energy
        if self.hvac_on:
            temp_diff = abs(self.current_temp - self.user_preferences['preferred_temp'])
            energy += 1.8 + (temp_diff * 0.25)
        
        # Lighting energy
        energy += (self.lighting / 100.0) * 0.4
        
        # Occupancy adds appliances
        if self.occupancy:
            hour = self.current_time
            if 6 <= hour < 9:  # Morning (cooking, getting ready)
                energy += np.random.uniform(0.8, 1.5)
            elif 18 <= hour < 23:  # Evening (cooking, TV, etc)
                energy += np.random.uniform(1.0, 2.0)
            else:
                energy += np.random.uniform(0.2, 0.6)
        else:
            energy += np.random.uniform(0.1, 0.3)
        
        self.energy_usage = energy
        return energy
    
    def step(self, action):
        """Execute one step"""
        self.step_count += 1
        
        # Update time (15 min per step = 4 steps/hour)
        self.current_time += 0.25
        if self.current_time >= 24:
            self.current_time = 0
            self.day_count += 1
            
            # Change seasons
            if self.day_count % 90 == 0:
                seasons = ['spring', 'summer', 'fall', 'winter']
                self.season = seasons[(self.day_count // 90) % 4]
        
        # Update external factors
        self._update_weather()
        self._update_occupancy()
        
        # Execute action
        if action == 1:  # HVAC on
            self.hvac_on = True
        elif action == 2:  # HVAC off
            self.hvac_on = False
        elif action == 3:  # Light +
            self.lighting = min(100.0, self.lighting + 10.0)
        elif action == 4:  # Light -
            self.lighting = max(0.0, self.lighting - 10.0)
        
        # Update environment
        self._update_temperature()
        self._update_humidity()
        energy = self._calculate_energy()
        comfort = self._calculate_comfort()
        
        # Calculate reward
        reward = self._calculate_reward(comfort, energy)
        
        # Build observation
        obs = np.array([
            self.current_temp,
            self.current_humidity,
            self.current_time,
            comfort,
            float(self.hvac_on),
            self.lighting,
            energy
        ], dtype=np.float32)
        
        done = False  # Continuous
        
        info = {
            'weather': self.weather,
            'occupancy': self.occupancy,
            'outside_temp': self.outside_temp,
            'season': self.season,
            'user_prefs': self.user_preferences
        }
        
        return obs, reward, done, False, info
    
    def _calculate_reward(self, comfort, energy):
        """Reward function considering user preferences"""
        # Comfort is primary goal
        comfort_reward = comfort * 10.0
        
        # Energy cost (scaled by user's consciousness)
        energy_penalty = -energy * self.user_preferences['energy_conscious'] * 0.8
        
        # Bonus for excellent comfort
        if comfort > 0.85:
            comfort_reward += 3.0
        
        # Heavy penalty for poor comfort when home
        if comfort < 0.4 and self.occupancy:
            comfort_reward -= 5.0
        
        return comfort_reward + energy_penalty
    
    def reset(self, seed=None):
        """Reset with new random conditions"""
        if seed:
            np.random.seed(seed)
        
        # Generate new user (different preferences)
        self.user_preferences = self._generate_user_preferences()
        
        # Random starting state
        self.current_temp = np.random.uniform(18, 28)
        self.current_humidity = np.random.uniform(40, 70)
        self.current_time = np.random.uniform(0, 24)
        self.hvac_on = False
        self.lighting = 50.0
        
        self.weather = np.random.choice(['sunny', 'cloudy', 'rainy'])
        self.outside_temp = np.random.uniform(15, 30)
        self.season = np.random.choice(['spring', 'summer', 'fall', 'winter'])
        
        self._update_occupancy()
        self.energy_usage = self._calculate_energy()
        comfort = self._calculate_comfort()
        
        obs = np.array([
            self.current_temp,
            self.current_humidity,
            self.current_time,
            comfort,
            float(self.hvac_on),
            self.lighting,
            self.energy_usage
        ], dtype=np.float32)
        
        return obs, {}

if __name__ == "__main__":
    # Test
    env = RealisticSmartHomeEnv()
    obs, _ = env.reset()
    
    print("🏠 Realistic Smart Home Environment Test\n")
    print("User Preferences (Simulated Learning):")
    for k, v in env.user_preferences.items():
        print(f"  {k}: {v:.2f}")
    print()
    
    for i in range(10):
        action = env.action_space.sample()
        obs, reward, done, _, info = env.step(action)
        
        print(f"Step {i+1}:")
        print(f"  Time: {obs[2]:.1f}h | Temp: {obs[0]:.1f}°C | Comfort: {obs[3]:.2f}")
        print(f"  Weather: {info['weather']} | Occupancy: {info['occupancy']}")
        print(f"  Reward: {reward:.2f}\n")
