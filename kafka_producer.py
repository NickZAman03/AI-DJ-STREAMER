#!/usr/bin/env python3
"""
Kafka Producer for AI DJ Streamer
Sends live chat messages to the 'live-chat' topic every 2 seconds
"""

import json
import time
import random
import sys
from confluent_kafka import Producer
from datetime import datetime

# Import Kafka configuration
try:
    from kafka_config import KAFKA_CONFIG, KAFKA_TOPIC
except ImportError:
    print("❌ Error: kafka_config.py not found!")
    print("Please create kafka_config.py with your Confluent Cloud credentials.")
    sys.exit(1)

# Live chat messages to send
MESSAGES = [
    "This beat is lit!",
    "I'm feeling so low today.",
    "This makes me wanna dance!",
    "Ugh, not in the mood.",
    "Such a peaceful vibe here.",
    "Wow this is fire 🔥",
    "I'm bored out of my mind",
    "This is straight up art."
]

def validate_config():
    """Validate that Kafka configuration has been properly set"""
    placeholder_values = ['YOUR_BOOTSTRAP_SERVER', 'YOUR_API_KEY', 'YOUR_API_SECRET']
    
    for key, value in KAFKA_CONFIG.items():
        if value in placeholder_values:
            print(f"❌ Error: {key} still has placeholder value: {value}")
            print("Please update kafka_config.py with your actual Confluent Cloud credentials.")
            return False
    
    print("✅ Kafka configuration validated successfully!")
    return True

def delivery_report(err, msg):
    """Delivery report callback for Kafka messages"""
    if err is not None:
        print(f'❌ Message delivery failed: {err}')
    else:
        print(f'✅ Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')
        print(f'📝 Message: {msg.value().decode("utf-8")}')

def create_message_payload(message):
    """Create a structured message payload with metadata"""
    return {
        'message': message,
        'timestamp': datetime.now().isoformat(),
        'user_id': f'user_{random.randint(1000, 9999)}',
        'session_id': f'session_{random.randint(10000, 99999)}',
        'platform': 'ai-dj-streamer'
    }

def main():
    """Main function to run the Kafka producer"""
    print("🚀 Starting AI DJ Streamer Kafka Producer")
    print(f"📡 Connecting to Kafka topic: {KAFKA_TOPIC}")
    print(f"📝 Will send {len(MESSAGES)} different messages in rotation")
    print("⏱️  Sending messages every 2 seconds...")
    print("-" * 50)
    
    # Validate configuration
    if not validate_config():
        sys.exit(1)
    
    # Create Kafka producer
    try:
        producer = Producer(KAFKA_CONFIG)
        print("✅ Kafka producer created successfully!")
    except Exception as e:
        print(f"❌ Failed to create Kafka producer: {e}")
        print("Please check your Confluent Cloud credentials in kafka_config.py")
        sys.exit(1)
    
    message_index = 0
    total_messages_sent = 0
    
    try:
        while True:
            # Get current message
            current_message = MESSAGES[message_index % len(MESSAGES)]
            
            # Create message payload
            payload = create_message_payload(current_message)
            message_json = json.dumps(payload, ensure_ascii=False)
            
            # Send message to Kafka
            producer.produce(
                topic=KAFKA_TOPIC,
                value=message_json.encode('utf-8'),
                callback=delivery_report
            )
            
            # Flush messages to ensure delivery
            producer.flush()
            
            # Update counters
            message_index += 1
            total_messages_sent += 1
            
            print(f"📊 Total messages sent: {total_messages_sent}")
            print(f"🔄 Next message in 2 seconds...")
            print("-" * 30)
            
            # Wait 2 seconds before next message
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping Kafka producer...")
        print(f"📈 Total messages sent: {total_messages_sent}")
        producer.flush()
        print("✅ Producer stopped gracefully")
    except Exception as e:
        print(f"❌ Error: {e}")
        producer.flush()

if __name__ == "__main__":
    main() 