import sqlite3
import json
import paho.mqtt.client as mqtt

# 1. Initialize Local SQLite Database (Raw Data Archive)
DB_PATH = "../db/local_archive.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            topic TEXT,
            payload JSON
        )
    ''')
    conn.commit()
    conn.close()

# 2. Define Local MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to local RabbitMQ broker.")
        client.subscribe("factory/telemetry")
    else:
        print(f"RabbitMQ connection failed: {rc}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    topic = msg.topic
    print(f"\n[Local] Received on {topic}: {payload}")
    
    # Save raw data to SQLite instead of sending to Azure
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO telemetry (topic, payload) VALUES (?, ?)", (topic, payload))
        conn.commit()
        conn.close()
        print("[Storage] Saved to local SQLite archive.")
        
        # Here is where Thread B (Mediator) will eventually be triggered
        # to convert this JSON into Protobuf.
        
    except Exception as e:
        print(f"[Error] Failed to save to database: {e}")

# 3. Start the Local MQTT Client
init_db()
mqtt_client = mqtt.Client(client_id="edge_gateway_ingestion")
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to the RabbitMQ container via the Docker network
print("Starting Edge Ingestion Service...")
mqtt_client.connect("rabbitmq", 1883)

try:
    mqtt_client.loop_forever()
except KeyboardInterrupt:
    print("\nDisconnecting...")
    mqtt_client.disconnect()