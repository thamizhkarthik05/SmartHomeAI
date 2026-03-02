import gymnasium as gym
from gymnasium import spaces
import numpy as np

class InteractiveSmartHomeEnv(gym.Env):
    """
    Interactive Smart Home Environment where actions have REAL effects!
    The agent's actions actually change temperature, lighting, comfort, and energy.
    """

    def __init__(self):
        super(InteractiveSmartHomeEnv, self).__init__()

        # Define action space
        # 0 = do nothing
        # 1 = turn HVAC on
        # 2 = turn HVAC off
        # 3 = increase light by 20%
        # 4 = decrease light by 20%
        self.action_space = spaces.Discrete(5)

        # Define observation space
        # [temperature, humidity, time_of_day, comfort, hvac_state, lighting, energy]
        low = np.array([15, 20, 0, 0, 0, 0, 0], dtype=np.float32)
        high = np.array([35, 80, 24, 1, 1, 100, 5], dtype=np.float32)
        self.observation_space = spaces.Box(low, high, dtype=np.float32)

        # Target ranges for comfort
        self.target_temp_range = (20, 24)  # Comfortable temperature
        self.target_light_range = (40, 80)  # Comfortable lighting

        # Initialize state
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        # Random initial conditions
        self.temperature = np.random.uniform(18, 28)
        self.humidity = np.random.uniform(30, 70)
        self.time_of_day = np.random.randint(0, 24)
        self.hvac_on = False
        self.lighting = np.random.uniform(20, 80)
        self.outside_temp = np.random.uniform(15, 32)
        
        # Calculate initial comfort and energy
        self.comfort = self._calculate_comfort()
        self.energy = self._calculate_energy()
        
        self.steps = 0
        
        return self._get_obs(), {}

    def _get_obs(self):
        obs = np.array([
            self.temperature,
            self.humidity,
            self.time_of_day,
            self.comfort,
            1 if self.hvac_on else 0,
            self.lighting,
            self.energy
        ], dtype=np.float32)
        return obs

    def _calculate_comfort(self):
        """Calculate comfort score based on temperature and lighting"""
        comfort = 0.0
        
        # Temperature comfort (0 to 0.6)
        if self.target_temp_range[0] <= self.temperature <= self.target_temp_range[1]:
            temp_comfort = 0.6
        else:
            # Discomfort increases with distance from target
            distance = min(abs(self.temperature - self.target_temp_range[0]),
                          abs(self.temperature - self.target_temp_range[1]))
            temp_comfort = max(0, 0.6 - distance * 0.1)
        
        # Lighting comfort (0 to 0.4)
        # Adjust target based on time of day
        if 22 <= self.time_of_day or self.time_of_day < 6:  # Night
            target_light = (0, 30)
        elif 6 <= self.time_of_day < 9:  # Morning
            target_light = (40, 70)
        else:  # Day/Evening
            target_light = (60, 90)
        
        if target_light[0] <= self.lighting <= target_light[1]:
            light_comfort = 0.4
        else:
            distance = min(abs(self.lighting - target_light[0]),
                          abs(self.lighting - target_light[1]))
            light_comfort = max(0, 0.4 - distance * 0.005)
        
        comfort = temp_comfort + light_comfort
        return min(1.0, comfort)

    def _calculate_energy(self):
        """Calculate energy consumption"""
        energy = 0.5  # Base consumption
        
        if self.hvac_on:
            # More energy if HVAC is fighting outside temperature
            temp_diff = abs(self.temperature - self.outside_temp)
            energy += 1.0 + (temp_diff * 0.05)
        
        # Lighting energy
        energy += self.lighting * 0.01
        
        return energy

    def step(self, action):
        self.steps += 1
        
        # --- ACTIONS HAVE REAL EFFECTS ---
        
        if action == 1:  # Turn HVAC ON
            self.hvac_on = True
        elif action == 2:  # Turn HVAC OFF
            self.hvac_on = False
        elif action == 3:  # Increase lighting
            self.lighting = min(100, self.lighting + 20)
        elif action == 4:  # Decrease lighting
            self.lighting = max(0, self.lighting - 20)
        
        # --- SIMULATE PHYSICS ---
        
        # Temperature changes based on HVAC and outside influence
        if self.hvac_on:
            # HVAC pulls temperature toward comfortable range
            target_temp = (self.target_temp_range[0] + self.target_temp_range[1]) / 2
            self.temperature += (target_temp - self.temperature) * 0.3
        else:
            # Temperature drifts toward outside temperature
            self.temperature += (self.outside_temp - self.temperature) * 0.05
        
        # Add some random variation
        self.temperature += np.random.normal(0, 0.2)
        self.temperature = np.clip(self.temperature, 15, 35)
        
        # Humidity changes slightly
        self.humidity += np.random.normal(0, 1)
        self.humidity = np.clip(self.humidity, 20, 80)
        
        # Time advances
        self.time_of_day = (self.time_of_day + 1) % 24
        
        # Update comfort and energy based on new state
        old_comfort = self.comfort
        self.comfort = self._calculate_comfort()
        self.energy = self._calculate_energy()
        
        # --- REWARD FUNCTION (IMPROVED!) ---
        reward = 0
        
        # BIG reward for high comfort
        reward += self.comfort * 20
        
        # Bonus for improving comfort
        comfort_improvement = self.comfort - old_comfort
        if comfort_improvement > 0:
            reward += comfort_improvement * 30
        
        # Moderate energy penalty
        reward -= self.energy * 1.5
        
        # Small bonus for being in target ranges
        if self.target_temp_range[0] <= self.temperature <= self.target_temp_range[1]:
            reward += 5
        
        # Appropriate lighting for time of day
        if 22 <= self.time_of_day or self.time_of_day < 6:  # Night
            if self.lighting < 30:
                reward += 3
        elif 9 <= self.time_of_day < 18:  # Day
            if self.lighting > 60:
                reward += 3
        
        # NO action penalty! We want the agent to take actions when needed
        
        # Episode ends after 100 steps or if comfort is very poor
        terminated = self.steps >= 100
        
        return self._get_obs(), reward, terminated, False, {}

    def render(self, mode="human"):
        print(
            f"Step: {self.steps}, "
            f"Temp: {self.temperature:.1f}°C, "
            f"Light: {self.lighting:.0f}%, "
            f"HVAC: {'ON' if self.hvac_on else 'OFF'}, "
            f"Comfort: {self.comfort:.3f}, "
            f"Energy: {self.energy:.2f}kW"
        )

    def close(self):
        pass
