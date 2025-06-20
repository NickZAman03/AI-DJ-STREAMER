#!/usr/bin/env python3
"""Script to set environment variables for testing"""

import os

# Set environment variables
os.environ['CONFLUENT_BOOTSTRAP_SERVERS'] = 'pkc-921jm.us-east-2.aws.confluent.cloud:9092'
os.environ['CONFLUENT_API_KEY'] = 'WAN53PYS2HCN2U7B'
os.environ['CONFLUENT_API_SECRET'] = 'MJvuq2fBr2OU5MiEvRwOxiBVF5NRdVUlqbFp1uXH2s6k3DMLphXJ5fZrpEGX9V'
os.environ['KAFKA_TOPIC'] = 'live-chat'
os.environ['PORT'] = '8002'

print("✅ Environment variables set successfully!")
print(f"CONFLUENT_BOOTSTRAP_SERVERS: {os.environ.get('CONFLUENT_BOOTSTRAP_SERVERS')}")
print(f"CONFLUENT_API_KEY: {os.environ.get('CONFLUENT_API_KEY')}")
print(f"CONFLUENT_API_SECRET: {os.environ.get('CONFLUENT_API_SECRET', '***HIDDEN***')}")
print(f"KAFKA_TOPIC: {os.environ.get('KAFKA_TOPIC')}")
print(f"PORT: {os.environ.get('PORT')}") 