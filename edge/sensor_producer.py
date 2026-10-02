import time
import json
import random
import paho.mqtt.client as mqtt

client = mqtt.Client(client_id="motor_sensor_01")

# 1. Connect to RabbitMQ with retry logic
while True:
    try:
        client.connect("rabbitmq", 1883)
        print("Successfully connected to RabbitMQ!")
        break
    except ConnectionRefusedError:
        print("RabbitMQ is not ready yet. Retrying in 3 seconds...")
        time.sleep(3)

# 2. Start the network daemon in the background
client.loop_start()

# 3. Generate and publish telemetry every 5 seconds
print("Starting telemetry transmission...")
while True:
    payload = {
        "sensor_id": "motor_sensor_01",
        "temperature": round(random.uniform(20.0, 30.0), 2),
        "timestamp": int(time.time())
    }
    
    # Publish to the MQTT topic
    client.publish("factory/telemetry", json.dumps(payload))
    print(f"[Sensor] Published: {payload}")
    
    # Wait 5 seconds before sending the next one
    time.sleep(5)