from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from textblob import TextBlob
import nltk
import os
from typing import List, Dict
import json
from fastapi import Request
from fastapi import Body
import random
import threading
import queue

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Set environment variables for local development (if not already set)
if not os.getenv('CONFLUENT_BOOTSTRAP_SERVERS'):
    os.environ['CONFLUENT_BOOTSTRAP_SERVERS'] = 'pkc-921jm.us-east-2.aws.confluent.cloud:9092'
    os.environ['CONFLUENT_API_KEY'] = 'WAN53PYS2HCN2U7B'
    os.environ['CONFLUENT_API_SECRET'] = 'MJvuq2fBr2OU5MiEvRwOxiBVF5NRdVUlqbFp1uXH2s6k3DMLphXJ5fZrpEGX9V'
    os.environ['KAFKA_TOPIC'] = 'live-chat'

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

app = FastAPI(title="AI DJ Streamer", version="1.0.0")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic models
class ChatMessage(BaseModel):
    text: str
    timestamp: str = None

class MoodResponse(BaseModel):
    mood: str
    confidence: float
    music_vibe: str
    suggested_genres: List[str]

# Music vibe mapping based on mood
MOOD_TO_MUSIC = {
    "very_positive": {
        "vibe": "Energetic and Uplifting",
        "genres": ["Pop", "Dance", "House", "EDM", "Funk"]
    },
    "positive": {
        "vibe": "Happy and Upbeat",
        "genres": ["Pop", "Rock", "Indie", "Reggae", "Ska"]
    },
    "neutral": {
        "vibe": "Chill and Relaxed",
        "genres": ["Ambient", "Lo-fi", "Jazz", "Classical", "Folk"]
    },
    "negative": {
        "vibe": "Melancholic and Introspective",
        "genres": ["Blues", "Soul", "Alternative", "Indie Rock", "Acoustic"]
    },
    "very_negative": {
        "vibe": "Dark and Intense",
        "genres": ["Metal", "Rock", "Industrial", "Gothic", "Punk"]
    }
}

def analyze_mood(text: str) -> Dict:
    """Analyze the mood of the given text using TextBlob sentiment analysis."""
    blob = TextBlob(text.lower())
    polarity = blob.sentiment.polarity
    
    # Determine mood category
    if polarity >= 0.5:
        mood = "very_positive"
    elif polarity >= 0.1:
        mood = "positive"
    elif polarity >= -0.1:
        mood = "neutral"
    elif polarity >= -0.5:
        mood = "negative"
    else:
        mood = "very_negative"
    
    # Calculate confidence (absolute polarity value)
    confidence = abs(polarity)
    
    return {
        "mood": mood,
        "confidence": confidence,
        "polarity": polarity
    }

def get_music_recommendation(mood: str, confidence: float) -> Dict:
    """Get music recommendations based on mood analysis."""
    if mood in MOOD_TO_MUSIC:
        music_info = MOOD_TO_MUSIC[mood]
        return {
            "vibe": music_info["vibe"],
            "genres": music_info["genres"],
            "intensity": "High" if confidence > 0.7 else "Medium" if confidence > 0.3 else "Low"
        }
    else:
        return {
            "vibe": "Eclectic Mix",
            "genres": ["Pop", "Rock", "Electronic"],
            "intensity": "Medium"
        }

def suggest_music(mood: str) -> str:
    mood_tracks = {
        "happy": ["Upbeat EDM", "Feel Good Pop"],
        "sad": ["Lofi Rain", "Melancholy Piano"],
        "angry": ["Hard Rock", "Rap Battle"],
        "excited": ["Dance Party Mix", "High Energy Beats"],
        "neutral": ["Ambient Chill", "Lo-Fi Instrumentals"],
    }
    tracks = mood_tracks.get(mood, ["Eclectic Mix"])
    return random.choice(tracks)

@app.get("/")
async def read_root():
    """Serve the main HTML page."""
    return FileResponse("static/index.html")

@app.post("/analyze-mood", response_model=MoodResponse)
async def analyze_chat_mood(message: ChatMessage):
    """Analyze the mood of a chat message and return music recommendations."""
    try:
        # Analyze mood
        mood_analysis = analyze_mood(message.text)
        
        # Get music recommendations
        music_rec = get_music_recommendation(mood_analysis["mood"], mood_analysis["confidence"])
        
        return MoodResponse(
            mood=mood_analysis["mood"].replace("_", " ").title(),
            confidence=round(mood_analysis["confidence"], 3),
            music_vibe=music_rec["vibe"],
            suggested_genres=music_rec["genres"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing mood: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "ai-dj-streamer"}

@app.post("/mood")
async def get_mood(request: Request, body: dict = Body(...)):
    """
    Accepts JSON { "text": "I'm so excited!" }
    Returns { "mood": "happy", "suggested_track": "Upbeat EDM" }
    """
    text = body.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="Missing 'text' in request body.")
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    # Simple mapping with more moods - Fixed thresholds
    if polarity > 0.5:
        mood = "excited"
    elif polarity > 0.2:
        mood = "happy"
    elif polarity < -0.5:
        mood = "angry"
    elif polarity < -0.2:
        mood = "sad"
    else:
        mood = "neutral"  # This now covers -0.2 <= polarity <= 0.2
    suggested_track = suggest_music(mood)
    return {"mood": mood, "suggested_track": suggested_track}

# Shared queue for SSE
sse_result_queue = queue.Queue()

# Global flag to control consumer thread
consumer_running = False
consumer_thread = None

@app.on_event("startup")
def start_consumer():
    """Start the Kafka consumer in a background thread."""
    global consumer_running, consumer_thread
    
    try:
        from kafka_consumer import consume_messages, shared_result_queue
        # Set the shared queue for SSE
        import kafka_consumer
        kafka_consumer.shared_result_queue = sse_result_queue
        
        # Create a non-daemon thread to prevent shutdown issues
        consumer_thread = threading.Thread(
            target=consume_messages, 
            kwargs={"result_queue": sse_result_queue},
            name="kafka-consumer"
        )
        consumer_thread.daemon = False  # Don't make it a daemon thread
        consumer_running = True
        consumer_thread.start()
        print("✅ Kafka consumer started successfully in background thread")
        
    except Exception as e:
        print(f"❌ Failed to start Kafka consumer: {e}")
        print("⚠️  SSE streaming will not be available, but the API will still work")

@app.on_event("shutdown")
def stop_consumer():
    """Stop the Kafka consumer gracefully."""
    global consumer_running, consumer_thread
    
    if consumer_running and consumer_thread:
        consumer_running = False
        print("🛑 Stopping Kafka consumer...")
        # The consumer will exit when the thread is terminated

# SSE endpoint
@app.get("/stream")
async def stream(request: Request):
    async def event_generator():
        while True:
            # If client disconnects, break
            if await request.is_disconnected():
                break
            try:
                # Wait for a new result from the queue
                result = sse_result_queue.get(timeout=10)
                yield f"data: {json.dumps(result, ensure_ascii=False)}\n\n"
            except queue.Empty:
                # Send a keep-alive comment to prevent timeouts
                yield ": keep-alive\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 