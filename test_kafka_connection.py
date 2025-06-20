#!/usr/bin/env python3
"""Test Kafka connection to Confluent Cloud"""

import os
from confluent_kafka import Producer, Consumer, KafkaError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_producer_connection():
    """Test producer connection"""
    print("🧪 Testing Producer Connection...")
    
    # Get config from environment or fallback to new credentials
    bootstrap_servers = os.getenv('CONFLUENT_BOOTSTRAP_SERVERS', 'pkc-41p56.asia-south1.gcp.confluent.cloud:9092')
    api_key = os.getenv('CONFLUENT_API_KEY', 'QFPRKE7R65LCROC2')
    api_secret = os.getenv('CONFLUENT_API_SECRET', '36Q8gjZhYTnwFlbENZqoa91BuHIyOipkHm/LjbFf8NFsF+IafYcgHuFY6VatZ9WQ')
    
    config = {
        'bootstrap.servers': bootstrap_servers,
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'PLAIN',
        'sasl.username': api_key,
        'sasl.password': api_secret
    }
    
    print(f"🔗 Connecting to: {bootstrap_servers}")
    print(f"🔑 API Key: {api_key}")
    print(f"🔐 API Secret: {api_secret[:10]}...")
    
    try:
        producer = Producer(config)
        print("✅ Producer created successfully!")
        
        # Test a simple message
        topic = os.getenv('KAFKA_TOPIC', 'live-chat')
        test_message = "Test connection message"
        
        producer.produce(topic, test_message.encode('utf-8'))
        producer.flush()
        print(f"✅ Message sent to topic: {topic}")
        
        producer.close()
        return True
        
    except Exception as e:
        print(f"❌ Producer connection failed: {e}")
        return False

def test_consumer_connection():
    """Test consumer connection"""
    print("\n🧪 Testing Consumer Connection...")
    
    # Get config from environment or fallback to new credentials
    bootstrap_servers = os.getenv('CONFLUENT_BOOTSTRAP_SERVERS', 'pkc-41p56.asia-south1.gcp.confluent.cloud:9092')
    api_key = os.getenv('CONFLUENT_API_KEY', 'QFPRKE7R65LCROC2')
    api_secret = os.getenv('CONFLUENT_API_SECRET', '36Q8gjZhYTnwFlbENZqoa91BuHIyOipkHm/LjbFf8NFsF+IafYcgHuFY6VatZ9WQ')
    
    config = {
        'bootstrap.servers': bootstrap_servers,
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'PLAIN',
        'sasl.username': api_key,
        'sasl.password': api_secret,
        'group.id': 'test-group',
        'auto.offset.reset': 'latest'
    }
    
    try:
        consumer = Consumer(config)
        topic = os.getenv('KAFKA_TOPIC', 'live-chat')
        consumer.subscribe([topic])
        print(f"✅ Consumer subscribed to topic: {topic}")
        
        # Try to poll for a short time
        msg = consumer.poll(5.0)
        if msg is None:
            print("✅ Consumer polling works (no messages, which is expected)")
        else:
            print(f"✅ Consumer received message: {msg.value().decode('utf-8')}")
        
        consumer.close()
        return True
        
    except Exception as e:
        print(f"❌ Consumer connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Confluent Cloud Kafka Connection")
    print("=" * 50)
    
    producer_success = test_producer_connection()
    consumer_success = test_consumer_connection()
    
    print("\n" + "=" * 50)
    if producer_success and consumer_success:
        print("🎉 All tests passed! Your credentials are working.")
    else:
        print("❌ Some tests failed. Please check your credentials.")
        print("\n💡 Next steps:")
        print("1. Go to Confluent Cloud Console")
        print("2. Navigate to your cluster")
        print("3. Go to 'Clients' section")
        print("4. Select 'Python' and copy fresh credentials")
        print("5. Update your environment variables") 