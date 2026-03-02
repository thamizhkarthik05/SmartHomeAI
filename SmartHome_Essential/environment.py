import gymnasium as gym
from gymnasium import spaces
import pandas as pd
import numpy as np

class SmartHomeEnv(gym.Env):
    """
    Smart Home Environment for Reinforcement Learning
    The agent controls fan and lights to balance comfort and energy use.
    """

    def __init__(self, data_file="SmartHome_Environment_v1.csv"):
        super(SmartHomeEnv, self).__init__()

        # Load dataset
        self.df = pd.read_csv(data_file)

        # Convert fan_state (off/on) into numbers
        self.df["fan_state"] = self.df["fan_state"].apply(lambda x: 1 if str(x).lower() == "on" else 0)

        # Convert user_override_event (TRUE/FALSE) into numbers
        self.df["user_override_event"] = self.df["user_override_event"].apply(lambda x: 1 if str(x).upper() == "TRUE" else 0)

        self.current_step = 0

        # Define action space
        # 0 = do nothing
        # 1 = turn fan on
        # 2 = turn fan off
        # 3 = increase light by 20%
        # 4 = decrease light by 20%
        self.action_space = spaces.Discrete(5)

        # Define observation space
        # [room_temp, perceived_temp, light, comfort, fan_state, light_percent, energy]
        low = np.array([0, 0, 0, 0, 0, 0, 0], dtype=np.float32)
        high = np.array([40, 40, 2000, 1, 1, 100, 10], dtype=np.float32)
        self.observation_space = spaces.Box(low, high, dtype=np.float32)

    def _get_obs(self):
        row = self.df.iloc[self.current_step]
        obs = np.array([
            row["room_temperature_c"],
            row["perceived_temperature_c"],
            row["ambient_light_lux"],
            row["comfort_score"],
            row["fan_state"],
            row["light_state_percent"],
            row["energy_consumed_kw"]
        ], dtype=np.float32)
        return obs

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0
        return self._get_obs(), {}

    def step(self, action):
        row = self.df.iloc[self.current_step]

        # ----- Reward Function -----
        reward = 0

        # Encourage comfort
        reward += row["comfort_score"] * 10

        # Penalize energy usage
        reward -= row["energy_consumed_kw"] * 2

        # Penalize user overrides
        if row["user_override_event"] == 1:
            reward -= 20

        # Small penalty for making frequent changes (to simulate wear/tear)
        if action != 0:
            reward -= 0.5

        # Move to next step
        self.current_step += 1
        terminated = self.current_step >= len(self.df) - 1

        obs = self._get_obs() if not terminated else np.zeros(self.observation_space.shape, dtype=np.float32)

        return obs, reward, terminated, False, {}

    def render(self, mode="human"):
        row = self.df.iloc[self.current_step]
        print(
            f"Step: {self.current_step}, "
            f"Temp: {row['room_temperature_c']}C, "
            f"Light: {row['ambient_light_lux']} lux, "
            f"Comfort: {row['comfort_score']}, "
            f"Energy: {row['energy_consumed_kw']}kW"
        )

    def close(self):
        pass
