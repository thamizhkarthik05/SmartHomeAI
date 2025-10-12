import json
import time
import random
import threading
from datetime import datetime
import paho.mqtt.client as mqtt

class IoTDeviceSimulator:
    """
    Simulates IoT devices that would be used in real deployment
    """
    
    def __init__(self, device_id, device_type, room):
        self.device_id = device_id
        self.device_type = device_type  # 'fan', 'light', 'sensor'
        self.room = room
        self.state = {"status": "off", "value": 0}
        self.is_running = False
        
        # MQTT client for IoT communication simulation
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        
        # Device-specific properties
        if device_type == "fan":
            self.state = {"status": "off", "speed": 0}
        elif device_type == "light":
            self.state = {"status": "off", "brightness": 0}
        elif device_type == "sensor":
            self.state = {"temperature": 20.0, "humidity": 50.0, "light_level": 300}
    
    def on_connect(self, client, userdata, flags, rc):
        print(f"Device {self.device_id} connected to MQTT broker with result code {rc}")
        # Subscribe to commands for this device
        client.subscribe(f"smarthome/{self.room}/{self.device_type}/{self.device_id}/command")
    
    def on_message(self, client, userdata, msg):
        """Handle incoming MQTT commands"""
        try:
            command = json.loads(msg.payload.decode())
            self.execute_command(command)
        except Exception as e:
            print(f"Error processing command: {e}")
    
    def execute_command(self, command):
        """Execute a command sent to this device"""
        print(f"🔧 {self.device_id} executing: {command}")
        
        if self.device_type == "fan":
            if command.get("action") == "turn_on":
                self.state["status"] = "on"
                self.state["speed"] = command.get("speed", 1)
            elif command.get("action") == "turn_off":
                self.state["status"] = "off"
                self.state["speed"] = 0
                
        elif self.device_type == "light":
            if command.get("action") == "turn_on":
                self.state["status"] = "on"
                self.state["brightness"] = command.get("brightness", 100)
            elif command.get("action") == "turn_off":
                self.state["status"] = "off"
                self.state["brightness"] = 0
            elif command.get("action") == "set_brightness":
                if self.state["status"] == "on":
                    self.state["brightness"] = command.get("brightness", 50)
        
        # Publish state update
        self.publish_state()
    
    def publish_state(self):
        """Publish current device state"""
        topic = f"smarthome/{self.room}/{self.device_type}/{self.device_id}/state"
        payload = {
            "device_id": self.device_id,
            "timestamp": datetime.now().isoformat(),
            "room": self.room,
            "state": self.state
        }
        
        # Simulate network delay
        time.sleep(random.uniform(0.1, 0.3))
        
        print(f"📡 {self.device_id} state: {self.state}")
        # In real deployment, this would publish to MQTT broker
        # self.mqtt_client.publish(topic, json.dumps(payload))
    
    def simulate_sensor_readings(self):
        """Continuously generate sensor data (for sensor devices)"""
        while self.is_running and self.device_type == "sensor":
            # Simulate realistic sensor variations
            base_temp = 20 + random.uniform(-2, 5)
            base_humidity = 45 + random.uniform(-10, 15)
            base_light = 200 + random.uniform(-50, 300)
            
            # Add some noise
            self.state["temperature"] = round(base_temp + random.uniform(-0.5, 0.5), 1)
            self.state["humidity"] = round(max(0, min(100, base_humidity + random.uniform(-2, 2))), 1)
            self.state["light_level"] = round(max(0, base_light + random.uniform(-20, 20)), 0)
            
            self.publish_state()
            time.sleep(5)  # Update every 5 seconds
    
    def start(self):
        """Start the device simulation"""
        self.is_running = True
        if self.device_type == "sensor":
            sensor_thread = threading.Thread(target=self.simulate_sensor_readings)
            sensor_thread.daemon = True
            sensor_thread.start()
        
        print(f"✅ {self.device_type} {self.device_id} started in {self.room}")
    
    def stop(self):
        """Stop the device simulation"""
        self.is_running = False
        print(f"🛑 {self.device_type} {self.device_id} stopped")

class SmartHomeIoTSimulator:
    """
    Manages multiple IoT devices and simulates a complete smart home system
    """
    
    def __init__(self):
        self.devices = {}
        self.rooms = ["living_room", "bedroom", "office", "kitchen"]
        self.setup_devices()
    
    def setup_devices(self):
        """Create simulated IoT devices for each room"""
        device_id = 1
        
        for room in self.rooms:
            # Add sensor
            sensor = IoTDeviceSimulator(f"sensor_{device_id}", "sensor", room)
            self.devices[f"sensor_{device_id}"] = sensor
            device_id += 1
            
            # Add fan
            fan = IoTDeviceSimulator(f"fan_{device_id}", "fan", room)
            self.devices[f"fan_{device_id}"] = fan
            device_id += 1
            
            # Add light
            light = IoTDeviceSimulator(f"light_{device_id}", "light", room)
            self.devices[f"light_{device_id}"] = light
            device_id += 1
    
    def send_command(self, device_id, command):
        """Send a command to a specific device"""
        if device_id in self.devices:
            self.devices[device_id].execute_command(command)
        else:
            print(f"❌ Device {device_id} not found")
    
    def get_device_states(self):
        """Get current state of all devices"""
        states = {}
        for device_id, device in self.devices.items():
            states[device_id] = {
                "room": device.room,
                "type": device.device_type,
                "state": device.state
            }
        return states
    
    def start_all_devices(self):
        """Start all device simulations"""
        for device in self.devices.values():
            device.start()
        print(f"🏠 Smart Home IoT Simulator started with {len(self.devices)} devices")
    
    def stop_all_devices(self):
        """Stop all device simulations"""
        for device in self.devices.values():
            device.stop()
        print("🏠 Smart Home IoT Simulator stopped")

# Example usage
if __name__ == "__main__":
    # Create and start IoT simulator
    iot_sim = SmartHomeIoTSimulator()
    iot_sim.start_all_devices()
    
    # Example commands
    time.sleep(2)
    
    # Turn on living room fan
    iot_sim.send_command("fan_2", {"action": "turn_on", "speed": 2})
    
    # Turn on bedroom light at 50% brightness
    iot_sim.send_command("light_6", {"action": "turn_on", "brightness": 50})
    
    # Let it run for a bit
    try:
        time.sleep(30)
    except KeyboardInterrupt:
        pass
    finally:
        iot_sim.stop_all_devices()