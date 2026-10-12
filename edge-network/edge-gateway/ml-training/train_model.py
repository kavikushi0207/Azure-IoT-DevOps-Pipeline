import sqlite3
import time
# import torch
# import torch.nn as nn

DB_PATH = "../db/local_archive.db"

def load_local_data():
    """Reads the cleaned/standardized data for local training."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # In the future, this will read your Protobuf files or cleaned SQL rows
    cursor.execute("SELECT * FROM telemetry ORDER BY timestamp DESC LIMIT 100")
    data = cursor.fetchall()
    conn.close()
    return data

def train_local_model(data):
    print(f"Training ML model on {len(data)} unencrypted local records...")
    # TODO: Implement PyTorch/TensorFlow FedAvg local training loop here
    
    # Simulate training time
    time.sleep(2)
    
    print("Training complete. Extracting raw model weights...")
    raw_weights = [0.15, -0.02, 1.45, 0.99] # Dummy weights
    return raw_weights

if __name__ == "__main__":
    print("Initializing Local ML Training Node...")
    while True:
        # 1. Load the latest local factory data
        training_data = load_local_data()
        
        if training_data:
            # 2. Train the model and get unencrypted weights
            weights = train_local_model(training_data)
            
            # 3. Pass weights to TenSEAL (FHE Encryption Module)
            # This is where your Azure IoT Hub connection will eventually go!
            print(f"Forwarding weights to encryption module: {weights}\n")
        
        # Wait for the next training window (e.g., hourly or daily micro-batches)
        time.sleep(60)