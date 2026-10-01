# Azure-IoT-DevOps-Pipeline
This project is a DevOps and research-driven simulation of a secure Smart Factory. It demonstrates an end-to-end data pipeline routing telemetry from local edge sensors via RabbitMQ into Azure (IoT Hub, Stream Analytics, CosmosDB). To ensure data privacy, the pipeline integrates Homomorphic Encryption (FHE), allowing cloud-based anomaly detection machine learning models to compute directly on encrypted ciphertext without exposing the raw data.

Core Tech Stack: Python, RabbitMQ (AMQP), Azure Cloud Solutions, Docker, GitHub Actions CI/CD, and TenSEAL (Homomorphic Encryption).
