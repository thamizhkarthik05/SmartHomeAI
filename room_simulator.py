"""
🏠 Interactive Smart Home Room Simulator
=========================================
This script simulates a real room environment with:
- Visual representation of the room
- Real-time AI model control
- Interactive controls to change environment
- Live feedback on temperature, lights, fans
"""

import pygame
import numpy as np
from stable_baselines3 import DQN
from environment import SmartHomeEnv
import time
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Home AI - Room Simulator")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (100, 149, 237)
RED = (255, 99, 71)
GREEN = (50, 205, 50)
YELLOW = (255, 215, 0)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (173, 216, 230)

# Fonts
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

class RoomSimulator:
    def __init__(self):
        # Load model
        try:
            self.model = DQN.load("smart_home_ai_brain.zip")
            print("✅ Model loaded successfully!")
        except:
            print("❌ Model not found! Please train the model first: python train.py")
            sys.exit(1)
        
        # Create environment
        self.env = SmartHomeEnv(data_file="SmartHome_Environment_v1.csv")
        self.obs, _ = self.env.reset()
        
        # Simulation state
        self.running = True
        self.paused = False
        self.auto_mode = True
        self.step_count = 0
        self.last_action = 0
        self.last_reward = 0
        self.total_reward = 0
        
        # Room state (derived from observation)
        self.room_temp = self.obs[0]
        self.light_level = self.obs[2]
        self.comfort = self.obs[3]
        self.fan_on = bool(self.obs[4])
        self.light_brightness = self.obs[5]
        self.energy = self.obs[6]
        
        # Animation
        self.fan_angle = 0
        self.light_pulse = 0
        
        # History for graphs
        self.temp_history = []
        self.comfort_history = []
        self.energy_history = []
        self.max_history = 50
        
        # Action names
        self.action_names = {
            0: "Do Nothing",
            1: "Turn Fan ON",
            2: "Turn Fan OFF",
            3: "Increase Light +20%",
            4: "Decrease Light -20%"
        }
    
    def get_temp_color(self, temp):
        """Get color based on temperature"""
        if temp < 20:
            return BLUE
        elif temp < 23:
            return LIGHT_BLUE
        elif temp < 26:
            return GREEN
        elif temp < 29:
            return ORANGE
        else:
            return RED
    
    def draw_room(self):
        """Draw the room visualization"""
        # Room background (color changes with temperature)
        room_color = self.get_temp_color(self.room_temp)
        room_color = tuple(int(c * 0.3) for c in room_color)  # Darken
        pygame.draw.rect(screen, room_color, (50, 50, 500, 500))
        pygame.draw.rect(screen, BLACK, (50, 50, 500, 500), 3)
        
        # Floor
        pygame.draw.rect(screen, DARK_GRAY, (50, 500, 500, 50))
        
        # Ceiling light
        light_x, light_y = 300, 100
        if self.light_brightness > 0:
            # Light glow effect
            for i in range(5):
                alpha = int(255 * (self.light_brightness / 100) * (1 - i/5))
                radius = int(40 + (self.light_brightness / 100) * 100 * (i+1))
                color = (255, 255, int(200 - self.light_brightness), alpha)
                s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
                pygame.draw.circle(s, color, (radius, radius), radius)
                screen.blit(s, (light_x - radius, light_y - radius))
        
        # Light bulb
        pygame.draw.circle(screen, YELLOW if self.light_brightness > 50 else GRAY, 
                         (light_x, light_y), 20)
        pygame.draw.circle(screen, BLACK, (light_x, light_y), 20, 2)
        
        # Fan
        fan_x, fan_y = 450, 100
        if self.fan_on:
            # Rotating fan blades
            for i in range(3):
                angle = self.fan_angle + i * 120
                end_x = fan_x + int(30 * np.cos(np.radians(angle)))
                end_y = fan_y + int(30 * np.sin(np.radians(angle)))
                pygame.draw.line(screen, DARK_GRAY, (fan_x, fan_y), (end_x, end_y), 5)
            self.fan_angle += 15 if not self.paused else 0
        else:
            # Static fan
            for i in range(3):
                angle = i * 120
                end_x = fan_x + int(30 * np.cos(np.radians(angle)))
                end_y = fan_y + int(30 * np.sin(np.radians(angle)))
                pygame.draw.line(screen, GRAY, (fan_x, fan_y), (end_x, end_y), 5)
        
        # Fan center
        pygame.draw.circle(screen, BLACK, (fan_x, fan_y), 10)
        
        # Temperature indicator (thermometer)
        therm_x, therm_y = 120, 250
        pygame.draw.rect(screen, WHITE, (therm_x, therm_y, 30, 150))
        pygame.draw.circle(screen, WHITE, (therm_x + 15, therm_y + 150), 20)
        
        # Mercury level
        temp_ratio = max(0, min(1, (self.room_temp - 15) / 25))
        mercury_height = int(150 * temp_ratio)
        mercury_color = self.get_temp_color(self.room_temp)
        pygame.draw.rect(screen, mercury_color, 
                        (therm_x + 5, therm_y + 150 - mercury_height, 20, mercury_height))
        pygame.draw.circle(screen, mercury_color, (therm_x + 15, therm_y + 150), 15)
        
        # Person icon (for comfort visualization)
        person_x, person_y = 300, 400
        person_color = GREEN if self.comfort > 0.7 else ORANGE if self.comfort > 0.5 else RED
        
        # Head
        pygame.draw.circle(screen, person_color, (person_x, person_y), 25)
        # Body
        pygame.draw.rect(screen, person_color, (person_x - 15, person_y + 25, 30, 60))
        # Arms
        pygame.draw.rect(screen, person_color, (person_x - 40, person_y + 30, 80, 15))
        # Legs
        pygame.draw.rect(screen, person_color, (person_x - 15, person_y + 85, 12, 40))
        pygame.draw.rect(screen, person_color, (person_x + 3, person_y + 85, 12, 40))
        
        # Comfort emoji
        if self.comfort > 0.7:
            emoji = "😊"
        elif self.comfort > 0.5:
            emoji = "😐"
        else:
            emoji = "😟"
        emoji_text = font_large.render(emoji, True, BLACK)
        screen.blit(emoji_text, (person_x - 20, person_y - 10))
    
    def draw_status_panel(self):
        """Draw status information panel"""
        panel_x = 600
        panel_y = 50
        
        # Panel background
        pygame.draw.rect(screen, GRAY, (panel_x, panel_y, 550, 600))
        pygame.draw.rect(screen, BLACK, (panel_x, panel_y, 550, 600), 3)
        
        # Title
        title = font_large.render("Room Status", True, BLACK)
        screen.blit(title, (panel_x + 20, panel_y + 10))
        
        y_offset = panel_y + 70
        
        # Temperature
        temp_text = font_medium.render(f"🌡️ Temperature: {self.room_temp:.1f}°C", True, BLACK)
        screen.blit(temp_text, (panel_x + 20, y_offset))
        y_offset += 50
        
        # Light level
        light_text = font_medium.render(f"💡 Light: {self.light_level:.0f} lux ({self.light_brightness:.0f}%)", 
                                       True, BLACK)
        screen.blit(light_text, (panel_x + 20, y_offset))
        y_offset += 50
        
        # Comfort score with bar
        comfort_text = font_medium.render(f"😊 Comfort: {self.comfort:.2f}", True, BLACK)
        screen.blit(comfort_text, (panel_x + 20, y_offset))
        y_offset += 35
        
        # Comfort bar
        bar_width = 300
        bar_height = 20
        pygame.draw.rect(screen, WHITE, (panel_x + 20, y_offset, bar_width, bar_height))
        comfort_width = int(bar_width * self.comfort)
        comfort_color = GREEN if self.comfort > 0.7 else ORANGE if self.comfort > 0.5 else RED
        pygame.draw.rect(screen, comfort_color, (panel_x + 20, y_offset, comfort_width, bar_height))
        pygame.draw.rect(screen, BLACK, (panel_x + 20, y_offset, bar_width, bar_height), 2)
        y_offset += 40
        
        # Energy consumption
        energy_text = font_medium.render(f"⚡ Energy: {self.energy:.2f} kW", True, BLACK)
        screen.blit(energy_text, (panel_x + 20, y_offset))
        y_offset += 50
        
        # Fan status
        fan_status = "ON 🌀" if self.fan_on else "OFF"
        fan_color = GREEN if self.fan_on else RED
        fan_text = font_medium.render(f"Fan: {fan_status}", True, fan_color)
        screen.blit(fan_text, (panel_x + 20, y_offset))
        y_offset += 60
        
        # AI Decision
        pygame.draw.line(screen, BLACK, (panel_x + 20, y_offset), (panel_x + 530, y_offset), 2)
        y_offset += 10
        
        ai_title = font_medium.render("🤖 AI Decision", True, BLUE)
        screen.blit(ai_title, (panel_x + 20, y_offset))
        y_offset += 40
        
        action_text = font_small.render(f"Action: {self.action_names[self.last_action]}", True, BLACK)
        screen.blit(action_text, (panel_x + 20, y_offset))
        y_offset += 30
        
        reward_text = font_small.render(f"Reward: {self.last_reward:.2f}", True, BLACK)
        screen.blit(reward_text, (panel_x + 20, y_offset))
        y_offset += 30
        
        total_reward_text = font_small.render(f"Total Reward: {self.total_reward:.2f}", True, BLACK)
        screen.blit(total_reward_text, (panel_x + 20, y_offset))
        y_offset += 40
        
        step_text = font_small.render(f"Step: {self.step_count}", True, BLACK)
        screen.blit(step_text, (panel_x + 20, y_offset))
    
    def draw_mini_graphs(self):
        """Draw small history graphs"""
        graph_x = 600
        graph_y = 500
        graph_w = 530
        graph_h = 140
        
        # Background
        pygame.draw.rect(screen, WHITE, (graph_x, graph_y, graph_w, graph_h))
        pygame.draw.rect(screen, BLACK, (graph_x, graph_y, graph_w, graph_h), 2)
        
        # Draw temperature history
        if len(self.temp_history) > 1:
            points = []
            for i, temp in enumerate(self.temp_history):
                x = int(graph_x + 10 + (i * (graph_w - 20) / len(self.temp_history)))
                y = int(graph_y + graph_h - 10 - ((temp - 15) / 25 * (graph_h - 20)))
                points.append((x, y))
            
            if len(points) > 1:
                pygame.draw.lines(screen, RED, False, points, 2)
        
        # Draw comfort history
        if len(self.comfort_history) > 1:
            points = []
            for i, comfort in enumerate(self.comfort_history):
                x = int(graph_x + 10 + (i * (graph_w - 20) / len(self.comfort_history)))
                y = int(graph_y + graph_h - 10 - (comfort * (graph_h - 20)))
                points.append((x, y))
            
            if len(points) > 1:
                pygame.draw.lines(screen, GREEN, False, points, 2)
        
        # Legend
        legend_temp = font_small.render("Temp", True, RED)
        legend_comfort = font_small.render("Comfort", True, GREEN)
        screen.blit(legend_temp, (graph_x + 10, graph_y + 5))
        screen.blit(legend_comfort, (graph_x + 80, graph_y + 5))
    
    def draw_controls(self):
        """Draw control instructions"""
        y = HEIGHT - 40
        
        # Mode indicator
        mode_text = "AUTO MODE (AI Controlling)" if self.auto_mode else "MANUAL MODE (Use Keys)"
        mode_color = GREEN if self.auto_mode else ORANGE
        mode_surface = font_small.render(mode_text, True, WHITE)
        mode_bg = pygame.Surface((mode_surface.get_width() + 20, 30))
        mode_bg.fill(mode_color)
        screen.blit(mode_bg, (10, y - 5))
        screen.blit(mode_surface, (20, y))
        
        # Controls
        controls = "SPACE: Pause | M: Toggle Auto/Manual | R: Reset | Q: Quit"
        if not self.auto_mode:
            controls += " | 0-4: Manual Actions"
        
        controls_text = font_small.render(controls, True, BLACK)
        screen.blit(controls_text, (300, y))
    
    def update_state(self, action):
        """Execute action and update state"""
        self.obs, reward, terminated, _, _ = self.env.step(action)
        
        # Update room state
        self.room_temp = self.obs[0]
        self.light_level = self.obs[2]
        self.comfort = self.obs[3]
        self.fan_on = bool(self.obs[4])
        self.light_brightness = self.obs[5]
        self.energy = self.obs[6]
        
        self.last_action = action
        self.last_reward = reward
        self.total_reward += reward
        self.step_count += 1
        
        # Update history
        self.temp_history.append(self.room_temp)
        self.comfort_history.append(self.comfort)
        self.energy_history.append(self.energy)
        
        if len(self.temp_history) > self.max_history:
            self.temp_history.pop(0)
            self.comfort_history.pop(0)
            self.energy_history.pop(0)
        
        if terminated:
            print("🏁 Simulation completed!")
            self.reset()
    
    def reset(self):
        """Reset simulation"""
        self.obs, _ = self.env.reset()
        self.step_count = 0
        self.total_reward = 0
        self.temp_history.clear()
        self.comfort_history.clear()
        self.energy_history.clear()
        self.last_action = 0
        self.last_reward = 0
    
    def run(self):
        """Main simulation loop"""
        clock = pygame.time.Clock()
        frame_count = 0
        
        print("\n" + "="*60)
        print("🏠 SMART HOME ROOM SIMULATOR")
        print("="*60)
        print("\nControls:")
        print("  SPACE - Pause/Resume")
        print("  M     - Toggle Auto/Manual mode")
        print("  R     - Reset simulation")
        print("  Q     - Quit")
        print("\nManual Mode Actions (when Auto is OFF):")
        print("  0 - Do Nothing")
        print("  1 - Turn Fan ON")
        print("  2 - Turn Fan OFF")
        print("  3 - Increase Light")
        print("  4 - Decrease Light")
        print("="*60 + "\n")
        
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_m:
                        self.auto_mode = not self.auto_mode
                    elif event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_q:
                        self.running = False
                    elif not self.auto_mode and event.key in [pygame.K_0, pygame.K_1, 
                                                               pygame.K_2, pygame.K_3, pygame.K_4]:
                        action = event.key - pygame.K_0
                        self.update_state(action)
            
            # Clear screen
            screen.fill(WHITE)
            
            # Draw everything
            self.draw_room()
            self.draw_status_panel()
            self.draw_mini_graphs()
            self.draw_controls()
            
            # Auto mode: AI makes decisions
            if self.auto_mode and not self.paused:
                frame_count += 1
                if frame_count % 30 == 0:  # Update every 30 frames (~0.5 seconds at 60 FPS)
                    action, _ = self.model.predict(self.obs, deterministic=True)
                    action = int(action)
                    self.update_state(action)
            
            pygame.display.flip()
            clock.tick(60)  # 60 FPS
        
        pygame.quit()
        print("\n👋 Simulation ended. Thanks for using Smart Home AI!")

if __name__ == "__main__":
    simulator = RoomSimulator()
    simulator.run()
