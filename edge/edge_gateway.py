import os
import json
import paho.mqtt.client as mqtt
from azure.iot.device import IoTHubDeviceClient, Message

# 1. Initialize the Azure IoT Hub Client
# We pull this securely from the Docker environment
CONNECTION_STRING = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
if not CONNECTION_STRING:
    raise ValueError("Missing IOTHUB_DEVICE_CONNECTION_STRING environment variable!")

print("Connecting to Azure IoT Hub...")
azure_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
azure_client.connect()
print("Azure connection established.")

# 2. Define Local MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to local RabbitMQ broker.")
        client.subscribe("factory/telemetry")
    else:
        print(f"RabbitMQ connection failed: {rc}")

def on_message(client, userdata, msg):
    # Decode the message from the local sensor
    payload = msg.payload.decode('utf-8')
    print(f"\n[Local] Received: {payload}")
    
    # Wrap the payload in an Azure Message object
    azure_msg = Message(payload)
    azure_msg.content_encoding = "utf-8"
    azure_msg.content_type = "application/json"
    
    # Forward the message to the Cloud
    print("[Cloud] Forwarding to Azure IoT Hub...")
    azure_client.send_message(azure_msg)
    print("[Cloud] Forwarding successful.")

# 3. Start the Local MQTT Client
mqtt_client = mqtt.Client(client_id="edge_gateway")
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to the RabbitMQ container via the Docker network
mqtt_client.connect("rabbitmq", 1883)

print("Gateway is listening for sensor data. Press CTRL+C to exit.")
try:
    mqtt_client.loop_forever()
except KeyboardInterrupt:
    print("\nDisconnecting...")
    azure_client.disconnect()
    mqtt_client.disconnect()