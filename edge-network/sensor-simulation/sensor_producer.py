import time
import json
import random
import paho.mqtt.client as mqtt

# Import our new encryption module
from encryption import HE_CONTEXT, encrypt_float, encrypt_vector
# Initialize the MQTT client for the sensor
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
    # Multiple metrics generated at the same timestamp
    temp = 24.8
    vib_x = 0.15
    vib_y = 0.42

# Encrypt the tuple together into ONE ciphertext
    metrics_tuple = (temp, vib_x, vib_y)
    encrypted_blob = encrypt_vector(HE_CONTEXT, metrics_tuple)
    # Create the payload with the encrypted temperature
    payload = {
        "sensor_id": "motor_sensor_01",
        "metrics_order": ["temperature", "vibration_x", "vibration_y"],
        "metrics_encrypted": encrypted_blob,
        "timestamp": int(time.time())
}
    
    client.publish("factory/telemetry", json.dumps(payload))
    
    # We print the raw temp locally just so you can verify what is happening
    print(f"[Sensor] Raw: {raw_temp}°C -> Encrypted Payload Sent.")
    
    time.sleep(5)