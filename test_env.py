#!/usr/bin/env python3
"""Test script to check environment variables"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Environment Variables Test:")
print("-" * 40)
print(f"CONFLUENT_BOOTSTRAP_SERVERS: {os.getenv('CONFLUENT_BOOTSTRAP_SERVERS')}")
print(f"CONFLUENT_API_KEY: {os.getenv('CONFLUENT_API_KEY')}")
print(f"CONFLUENT_API_SECRET: {os.getenv('CONFLUENT_API_SECRET', '***HIDDEN***')}")
print(f"KAFKA_TOPIC: {os.getenv('KAFKA_TOPIC', 'live-chat')}")
print(f"PORT: {os.getenv('PORT', '8000')}")
print("-" * 40)

# Test Kafka config function
try:
    from kafka_consumer import get_kafka_config
    config, topic = get_kafka_config()
    if config:
        print("✅ Kafka config loaded successfully!")
        print(f"Topic: {topic}")
        print(f"Bootstrap servers: {config.get('bootstrap.servers')}")
    else:
        print("❌ Kafka config failed to load")
except Exception as e:
    print(f"❌ Error testing Kafka config: {e}") 