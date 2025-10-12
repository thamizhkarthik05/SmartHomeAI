import json
import time
from stable_baselines3 import DQN
from multi_room_environment import MultiRoomSmartHomeEnv
from iot_device_simulator import SmartHomeIoTSimulator
import threading

class AIToIoTBridge:
    """
    Bridges the AI decision-making with IoT device control
    This simulates how the AI would control real IoT devices
    """
    
    def __init__(self, model_path="smart_home_ai_brain.zip"):
        # Load trained AI model
        self.ai_model = DQN.load(model_path)
        print("✅ AI Model loaded")
        
        # Create simulation environment
        self.env = MultiRoomSmartHomeEnv()
        print("✅ Environment loaded")
        
        # Create IoT device simulator
        self.iot_simulator = SmartHomeIoTSimulator()
        self.iot_simulator.start_all_devices()
        print("✅ IoT Simulator started")
        
        # Mapping between AI actions and IoT commands
        self.action_mapping = {
            0: None,  # Do nothing
            1: {"device_type": "fan", "command": {"action": "turn_on", "speed": 1}},
            2: {"device_type": "fan", "command": {"action": "turn_off"}},
            3: {"device_type": "light", "command": {"action": "set_brightness", "brightness": 80}},
            4: {"device_type": "light", "command": {"action": "set_brightness", "brightness": 40}}
        }
        
        self.rooms = ["living_room", "bedroom", "office", "kitchen"]
        self.is_running = False
        
    def ai_to_iot_command(self, room_id, action_id):
        """Convert AI action to IoT device command"""
        if action_id == 0:  # Do nothing
            return None
            
        room_name = self.rooms[room_id]
        action_info = self.action_mapping.get(action_id)
        
        if not action_info:
            return None
            
        # Find the appropriate device in the room
        device_type = action_info["device_type"]
        command = action_info["command"]
        
        # Find device ID for this room and type
        for device_id, device in self.iot_simulator.devices.items():
            if device.room == room_name and device.device_type == device_type:
                return device_id, command
                
        return None
    
    def run_ai_control_loop(self, duration_minutes=10):
        """Run the AI control loop for specified duration"""
        self.is_running = True
        obs, _ = self.env.reset()
        
        start_time = time.time()
        step_count = 0
        
        print(f"\n🤖 Starting AI Control Loop for {duration_minutes} minutes...")
        print("=" * 60)
        
        try:
            while self.is_running and (time.time() - start_time) < (duration_minutes * 60):
                # AI makes decision
                action, _ = self.ai_model.predict(obs, deterministic=True)
                room_id, device_action = action
                
                print(f"\n--- Step {step_count + 1} ---")
                print(f"🏠 Current room: {self.rooms[room_id]}")
                print(f"🤖 AI Decision: {device_action} (Room: {room_id})")
                
                # Convert AI action to IoT command
                iot_command = self.ai_to_iot_command(room_id, device_action)
                
                if iot_command:
                    device_id, command = iot_command
                    print(f"📡 Sending to {device_id}: {command}")
                    self.iot_simulator.send_command(device_id, command)
                else:
                    print("⏸️  No action taken")
                
                # Execute in environment
                obs, reward, terminated, _, info = self.env.step(action)
                print(f"💰 Reward: {reward:.2f}")
                
                # Show current room states
                room_states = info.get("room_states", {})
                for room, state in room_states.items():
                    temp_indicator = "🔥" if state["temp_offset"] > 0 else "❄️" if state["temp_offset"] < 0 else "🌡️"
                    light_indicator = "💡" if state["light_offset"] > 0 else "🔅" if state["light_offset"] < 0 else "💡"
                    fan_indicator = "🌀" if state["fan_on"] else "⏹️"
                    
                    print(f"  {room}: {temp_indicator} {state['temp_offset']:+.1f}°C | "
                          f"{light_indicator} {state['light_offset']:+.0f}% | {fan_indicator}")
                
                if terminated:
                    print("🏁 Simulation completed")
                    break
                
                step_count += 1
                time.sleep(2)  # Wait 2 seconds between decisions
                
        except KeyboardInterrupt:
            print("\n⏹️  Control loop interrupted by user")
        finally:
            self.stop()
    
    def get_system_status(self):
        """Get complete system status"""
        device_states = self.iot_simulator.get_device_states()
        room_states = self.env.get_room_status()
        
        status = {
            "timestamp": time.time(),
            "devices": device_states,
            "rooms": room_states,
            "ai_active": self.is_running
        }
        
        return status
    
    def manual_device_control(self, device_id, command):
        """Manual override for device control"""
        print(f"👤 Manual override: {device_id} -> {command}")
        self.iot_simulator.send_command(device_id, command)
    
    def stop(self):
        """Stop the AI control system"""
        self.is_running = False
        self.iot_simulator.stop_all_devices()
        print("🛑 AI-IoT Bridge stopped")

# CLI Interface
def main():
    print("🏠 Smart Home AI-IoT Bridge")
    print("=" * 40)
    
    try:
        bridge = AIToIoTBridge()
        
        while True:
            print("\nOptions:")
            print("1. Start AI Control Loop")
            print("2. Show System Status")
            print("3. Manual Device Control")
            print("4. Exit")
            
            choice = input("\nEnter choice (1-4): ").strip()
            
            if choice == "1":
                duration = input("Duration in minutes (default 5): ").strip()
                duration = int(duration) if duration.isdigit() else 5
                bridge.run_ai_control_loop(duration)
                
            elif choice == "2":
                status = bridge.get_system_status()
                print("\n📊 System Status:")
                print(json.dumps(status, indent=2, default=str))
                
            elif choice == "3":
                print("\nAvailable devices:")
                for device_id, device in bridge.iot_simulator.devices.items():
                    print(f"  {device_id}: {device.device_type} in {device.room}")
                
                device_id = input("Device ID: ").strip()
                if device_id in bridge.iot_simulator.devices:
                    print("Example commands:")
                    print('  Fan: {"action": "turn_on", "speed": 1}')
                    print('  Light: {"action": "turn_on", "brightness": 75}')
                    
                    command_str = input("Command (JSON): ").strip()
                    try:
                        command = json.loads(command_str)
                        bridge.manual_device_control(device_id, command)
                    except json.JSONDecodeError:
                        print("❌ Invalid JSON format")
                else:
                    print("❌ Device not found")
                    
            elif choice == "4":
                bridge.stop()
                break
                
            else:
                print("❌ Invalid choice")
                
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()