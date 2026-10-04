import time
import json
import random
import paho.mqtt.client as mqtt

# Import our new encryption module
from encryption import HE_CONTEXT, encrypt_float

client = mqtt.Client(client_id="motor_sensor_01")

while True:
    try:
        client.connect("rabbitmq", 1883)
        print("Successfully connected to RabbitMQ!")
        break
    except ConnectionRefusedError:
        print("RabbitMQ is not ready yet. Retrying in 3 seconds...")
        time.sleep(3)

client.loop_start()

print("Starting homomorphically encrypted telemetry transmission...")
while True:
    raw_temp = round(random.uniform(20.0, 30.0), 2)
    
    # Encrypt the temperature before it goes into the payload
    encrypted_temp_b64 = encrypt_float(HE_CONTEXT, raw_temp)
    
    payload = {
        "sensor_id": "motor_sensor_01",
        "temperature_encrypted": encrypted_temp_b64,
        "timestamp": int(time.time())
    }
    
    client.publish("factory/telemetry", json.dumps(payload))
    
    # We print the raw temp locally just so you can verify what is happening
    print(f"[Sensor] Raw: {raw_temp}°C -> Encrypted Payload Sent.")
    
    time.sleep(5)