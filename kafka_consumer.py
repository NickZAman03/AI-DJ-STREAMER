#!/usr/bin/env python3
"""
Kafka Consumer for AI DJ Streamer
Subscribes to 'live-chat' topic and analyzes mood of incoming messages
"""

import json
import time
import sys
from confluent_kafka import Consumer, KafkaError
from textblob import TextBlob
import random

# Shared queue for SSE streaming (to be set by main.py)
shared_result_queue = None

def analyze_mood(text: str) -> dict:
    """Analyze the mood of the given text using TextBlob sentiment analysis."""
    blob = TextBlob(text.lower())
    polarity = blob.sentiment.polarity
    
    # Determine mood category
    if polarity >= 0.5:
        mood = "excited"
    elif polarity >= 0.2:
        mood = "happy"
    elif polarity < -0.5:
        mood = "angry"
    elif polarity < -0.2:
        mood = "sad"
    else:
        mood = "neutral"
    
    # Calculate confidence (absolute polarity value)
    confidence = abs(polarity)
    
    return {
        "mood": mood,
        "confidence": confidence,
        "polarity": polarity
    }

def suggest_music(mood: str) -> str:
    """Get music recommendations based on mood analysis."""
    mood_tracks = {
        "happy": ["Upbeat EDM", "Feel Good Pop"],
        "sad": ["Lofi Rain", "Melancholy Piano"],
        "angry": ["Hard Rock", "Rap Battle"],
        "excited": ["Dance Party Mix", "High Energy Beats"],
        "neutral": ["Ambient Chill", "Lo-Fi Instrumentals"],
    }
    tracks = mood_tracks.get(mood, ["Eclectic Mix"])
    return random.choice(tracks)

def process_message(message_data, result_queue=None):
    """Process a single message: analyze mood and suggest music. Optionally put result in a queue."""
    try:
        # Extract the actual message text
        message_text = message_data.get('message', '')
        timestamp = message_data.get('timestamp', '')
        user_id = message_data.get('user_id', '')
        
        if not message_text:
            print("⚠️  Empty message received, skipping...")
            return
        
        # Analyze mood
        mood_analysis = analyze_mood(message_text)
        mood = mood_analysis["mood"]
        confidence = mood_analysis["confidence"]
        
        # Get music suggestion
        suggested_music = suggest_music(mood)
        
        # Prepare result for SSE streaming
        result = {
            "original_message": message_text,
            "mood": mood,
            "confidence": confidence,
            "suggested_track": suggested_music,
            "user_id": user_id,
            "timestamp": timestamp
        }
        
        # Print result
        print("=" * 80)
        print(f"📝 Text: {message_text}")
        print(f"😊 Mood: {mood.title()} (confidence: {confidence:.2f})")
        print(f"🎵 Music: {suggested_music}")
        print(f"👤 User: {user_id}")
        print(f"⏰ Time: {timestamp}")
        print("=" * 80)
        
        # Put result in queue for SSE if provided
        if result_queue is not None:
            try:
                result_queue.put(result, timeout=1)  # 1 second timeout
            except Exception as e:
                print(f"⚠️  Could not put result in queue: {e}")
        elif shared_result_queue is not None:
            try:
                shared_result_queue.put(result, timeout=1)  # 1 second timeout
            except Exception as e:
                print(f"⚠️  Could not put result in shared queue: {e}")
        
    except Exception as e:
        print(f"❌ Error processing message: {e}")

def consume_messages(result_queue=None):
    """Function to run the Kafka consumer in a background thread or as main. Optionally takes a queue."""
    try:
        from kafka_config import KAFKA_CONFIG, KAFKA_TOPIC
    except ImportError:
        print("❌ Error: kafka_config.py not found!")
        print("Please create kafka_config.py with your Confluent Cloud credentials.")
        return
    
    print("🎧 Starting AI DJ Streamer Kafka Consumer")
    print(f"📡 Subscribing to topic: {KAFKA_TOPIC}")
    print("⏱️  Polling for messages every second...")
    print("🔄 Ready to analyze mood and suggest music!")
    print("-" * 50)
    
    # Create Kafka consumer
    try:
        consumer = Consumer({
            **KAFKA_CONFIG,
            'group.id': 'ai-dj-streamer-group',
            'auto.offset.reset': 'latest',  # Start from latest messages
            'enable.auto.commit': True,
            'auto.commit.interval.ms': 1000
        })
        print("✅ Kafka consumer created successfully!")
    except Exception as e:
        print(f"❌ Failed to create Kafka consumer: {e}")
        print("Please check your Confluent Cloud credentials in kafka_config.py")
        return
    
    # Subscribe to topic
    try:
        consumer.subscribe([KAFKA_TOPIC])
        print(f"✅ Subscribed to topic: {KAFKA_TOPIC}")
    except Exception as e:
        print(f"❌ Failed to subscribe to topic: {e}")
        consumer.close()
        return
    
    messages_processed = 0
    
    try:
        while True:
            # Poll for messages
            msg = consumer.poll(1.0)  # Poll for 1 second
            
            if msg is None:
                # No message received
                continue
            elif msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    continue
                else:
                    print(f"❌ Consumer error: {msg.error()}")
                    continue
            
            try:
                # Parse the message
                message_json = msg.value().decode('utf-8')
                message_data = json.loads(message_json)
                
                # Process the message
                process_message(message_data, result_queue)
                messages_processed += 1
                
                print(f"📊 Total messages processed: {messages_processed}")
                print()
                
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse message JSON: {e}")
                print(f"Raw message: {msg.value()}")
            except Exception as e:
                print(f"❌ Error processing message: {e}")
                
    except KeyboardInterrupt:
        print("\n🛑 Stopping Kafka consumer...")
        print(f"📈 Total messages processed: {messages_processed}")
        consumer.close()
        print("✅ Consumer stopped gracefully")
    except Exception as e:
        print(f"❌ Error: {e}")
        consumer.close()
    finally:
        # Ensure consumer is always closed
        try:
            consumer.close()
            print("✅ Consumer closed")
        except:
            pass

if __name__ == "__main__":
    consume_messages() 