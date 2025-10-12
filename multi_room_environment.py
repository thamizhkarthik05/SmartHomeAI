import gymnasium as gym
from gymnasium import spaces
import pandas as pd
import numpy as np
import json

class MultiRoomSmartHomeEnv(gym.Env):
    """
    Multi-room Smart Home Environment with different room types and preferences
    """
    
    def __init__(self, data_file="SmartHome_Environment_v1.csv", config_file="rooms_config.json"):
        super(MultiRoomSmartHomeEnv, self).__init__()
        
        # Load base dataset
        self.df = pd.read_csv(data_file)
        self.df["fan_state"] = self.df["fan_state"].apply(lambda x: 1 if str(x).lower() == "on" else 0)
        self.df["user_override_event"] = self.df["user_override_event"].apply(lambda x: 1 if str(x).upper() == "TRUE" else 0)
        
        # Load room configuration
        try:
            with open(config_file, 'r') as f:
                self.rooms_config = json.load(f)
        except FileNotFoundError:
            # Default configuration
            self.rooms_config = {
                "living_room": {"temp_preference": 22, "light_preference": 60, "energy_weight": 1.0},
                "bedroom": {"temp_preference": 20, "light_preference": 30, "energy_weight": 1.5},
                "office": {"temp_preference": 21, "light_preference": 80, "energy_weight": 0.8},
                "kitchen": {"temp_preference": 23, "light_preference": 90, "energy_weight": 0.9}
            }
        
        self.rooms = list(self.rooms_config.keys())
        self.current_room = 0  # Start with first room
        self.current_step = 0
        
        # Action space: [room_id, action]
        # room_id: 0-3 (4 rooms), action: 0-4 (same as before)
        self.action_space = spaces.MultiDiscrete([len(self.rooms), 5])
        
        # Observation space: [room_temp, perceived_temp, light, comfort, fan_state, light_percent, energy, room_id]
        low = np.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=np.float32)
        high = np.array([40, 40, 2000, 1, 1, 100, 10, len(self.rooms)-1], dtype=np.float32)
        self.observation_space = spaces.Box(low, high, dtype=np.float32)
        
        # Initialize room states
        self.room_states = {room: {"temp_offset": 0, "light_offset": 0, "fan_on": 0} 
                           for room in self.rooms}
    
    def _get_obs(self):
        if self.current_step >= len(self.df):
            return np.zeros(8, dtype=np.float32)
            
        row = self.df.iloc[self.current_step]
        current_room_name = self.rooms[self.current_room]
        room_state = self.room_states[current_room_name]
        
        # Apply room-specific modifications
        modified_temp = row["room_temperature_c"] + room_state["temp_offset"]
        modified_light = max(0, min(100, row["light_state_percent"] + room_state["light_offset"]))
        
        # Calculate room-specific comfort based on preferences
        room_config = self.rooms_config[current_room_name]
        temp_diff = abs(modified_temp - room_config["temp_preference"])
        light_diff = abs(modified_light - room_config["light_preference"])
        comfort = max(0, 1 - (temp_diff/10 + light_diff/100))
        
        obs = np.array([
            modified_temp,
            row["perceived_temperature_c"],
            row["ambient_light_lux"],
            comfort,
            room_state["fan_on"],
            modified_light,
            row["energy_consumed_kw"] * room_config["energy_weight"],
            self.current_room
        ], dtype=np.float32)
        
        return obs
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0
        self.current_room = 0
        # Reset all room states
        for room in self.room_states:
            self.room_states[room] = {"temp_offset": 0, "light_offset": 0, "fan_on": 0}
        return self._get_obs(), {}
    
    def step(self, action):
        target_room_id, device_action = action
        target_room_name = self.rooms[target_room_id]
        
        # Apply action to target room
        if device_action == 1:  # Turn fan on
            self.room_states[target_room_name]["fan_on"] = 1
            self.room_states[target_room_name]["temp_offset"] -= 2  # Fan cools room
        elif device_action == 2:  # Turn fan off
            self.room_states[target_room_name]["fan_on"] = 0
            self.room_states[target_room_name]["temp_offset"] = max(-5, self.room_states[target_room_name]["temp_offset"])
        elif device_action == 3:  # Increase light
            self.room_states[target_room_name]["light_offset"] += 20
        elif device_action == 4:  # Decrease light
            self.room_states[target_room_name]["light_offset"] -= 20
        
        # Clamp values
        for room in self.room_states:
            self.room_states[room]["temp_offset"] = max(-5, min(5, self.room_states[room]["temp_offset"]))
            self.room_states[room]["light_offset"] = max(-50, min(50, self.room_states[room]["light_offset"]))
        
        # Calculate reward
        row = self.df.iloc[self.current_step]
        total_reward = 0
        
        # Reward based on all rooms
        for i, room_name in enumerate(self.rooms):
            room_config = self.rooms_config[room_name]
            room_state = self.room_states[room_name]
            
            # Room comfort
            temp = row["room_temperature_c"] + room_state["temp_offset"]
            light = max(0, min(100, row["light_state_percent"] + room_state["light_offset"]))
            
            temp_comfort = max(0, 1 - abs(temp - room_config["temp_preference"])/10)
            light_comfort = max(0, 1 - abs(light - room_config["light_preference"])/100)
            
            total_reward += (temp_comfort + light_comfort) * 5
            
            # Energy penalty
            energy_usage = room_state["fan_on"] * 0.5 + (room_state["light_offset"] > 0) * 0.3
            total_reward -= energy_usage * room_config["energy_weight"]
        
        # Move to next step and potentially next room
        self.current_step += 1
        self.current_room = (self.current_room + 1) % len(self.rooms)
        
        terminated = self.current_step >= len(self.df) - 1
        obs = self._get_obs() if not terminated else np.zeros(8, dtype=np.float32)
        
        return obs, total_reward, terminated, False, {"room_states": self.room_states.copy()}
    
    def render(self, mode="human"):
        print(f"\n--- Step {self.current_step} ---")
        for i, room_name in enumerate(self.rooms):
            room_state = self.room_states[room_name]
            marker = "👉 " if i == self.current_room else "   "
            print(f"{marker}{room_name}: Temp offset: {room_state['temp_offset']:+.1f}°C, "
                  f"Light offset: {room_state['light_offset']:+.0f}%, "
                  f"Fan: {'ON' if room_state['fan_on'] else 'OFF'}")
    
    def get_room_status(self):
        """Get current status of all rooms for dashboard"""
        return self.room_states.copy()