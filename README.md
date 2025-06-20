# 🎵 AI DJ Streamer

A real-time AI-powered music recommendation system that analyzes live chat sentiment and suggests music tracks based on the detected mood. Built with FastAPI, Kafka, and modern web technologies.

![AI DJ Streamer](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)
![Kafka](https://img.shields.io/badge/Kafka-Confluent-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

### 🎧 Real-time Mood Analysis
- **TextBlob Sentiment Analysis**: Analyzes chat messages for emotional content
- **5 Mood Categories**: Happy, Sad, Angry, Excited, Neutral
- **Confidence Scoring**: Provides confidence levels for mood detection

### 🎵 Intelligent Music Recommendations
- **Mood-based Suggestions**: Different music genres based on detected mood
- **Dynamic Track Selection**: Random selection from mood-appropriate playlists
- **Visual Music Player**: Mock player with progress bars and visualizers

### 📡 Real-time Streaming
- **Kafka Integration**: Confluent Cloud Kafka for message streaming
- **Server-Sent Events (SSE)**: Real-time updates to frontend
- **Live Feed**: Real-time display of analyzed messages and recommendations

### 🎨 Modern Web Interface
- **Responsive Design**: Works on desktop and mobile devices
- **Interactive UI**: Smooth animations and modern styling
- **Live Chat Simulation**: Built-in demo with predefined messages
- **Connection Status**: Real-time connection monitoring

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI       │    │   Kafka         │
│   (HTML/CSS/JS) │◄──►│   Backend       │◄──►│   Confluent     │
│                 │    │                 │    │   Cloud         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   EventSource   │    │   TextBlob      │    │   Producer      │
│   (SSE)         │    │   Analysis      │    │   (Messages)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Confluent Cloud account (free tier available)
- Modern web browser

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-dj-streamer.git
cd ai-dj-streamer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Kafka

Create a `kafka_config.py` file with your Confluent Cloud credentials:

```python
# kafka_config.py
KAFKA_CONFIG = {
    'bootstrap.servers': 'your-cluster.confluent.cloud:9092',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': 'your-api-key',
    'sasl.password': 'your-api-secret'
}

KAFKA_TOPIC = 'live-chat'
```

### 4. Create Kafka Topic

In your Confluent Cloud console, create a topic named `live-chat`.

### 5. Start the Application

#### Option A: All-in-One (Recommended for Development)
```bash
python -c "import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8002)"
```

#### Option B: Separate Components (Production)
```bash
# Terminal 1: Start FastAPI server
python -c "import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8002)"

# Terminal 2: Start Kafka producer
python kafka_producer.py

# Terminal 3: Start Kafka consumer (optional, handled by FastAPI)
python kafka_consumer.py
```

### 6. Open the Application

Navigate to [http://localhost:8002](http://localhost:8002) in your browser.

## 📖 Usage

### Manual Chat Analysis
1. Type a message in the chat input field
2. Click "Analyze Mood" or press Enter
3. View the mood analysis and music recommendations

### Live Chat Simulation
1. Click "🚀 Start Simulation" in the demo section
2. Watch as 10 predefined messages are processed in real-time
3. Observe the live feed for real-time updates

### Real-time Streaming
1. Start the Kafka producer to send live messages
2. Watch the "Live Feed" section for real-time updates
3. Each message shows:
   - Original text
   - Detected mood with emoji
   - Suggested music track
   - Timestamp

## 🔧 Configuration

### Environment Variables

Create a `.env` file for sensitive configuration:

```env
CONFLUENT_BOOTSTRAP_SERVERS=your-cluster.confluent.cloud:9092
CONFLUENT_API_KEY=your-api-key
CONFLUENT_API_SECRET=your-api-secret
KAFKA_TOPIC=live-chat
```

### Customizing Mood Analysis

Modify the mood thresholds in `main.py`:

```python
def analyze_mood(text: str) -> Dict:
    blob = TextBlob(text.lower())
    polarity = blob.sentiment.polarity
    
    # Customize these thresholds
    if polarity >= 0.5:
        mood = "very_positive"
    elif polarity >= 0.1:
        mood = "positive"
    # ... rest of the logic
```

### Adding Music Tracks

Update the music suggestions in `kafka_consumer.py`:

```python
def suggest_music(mood: str) -> str:
    mood_tracks = {
        "happy": ["Your Happy Track 1", "Your Happy Track 2"],
        "sad": ["Your Sad Track 1", "Your Sad Track 2"],
        # ... add more tracks
    }
    return random.choice(tracks)
```

## 📁 Project Structure

```
ai-dj-streamer/
├── main.py                 # FastAPI application with SSE endpoint
├── kafka_producer.py       # Kafka message producer
├── kafka_consumer.py       # Kafka message consumer with mood analysis
├── kafka_config.py         # Kafka configuration (create this)
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore             # Git ignore file
├── static/                # Frontend files
│   ├── index.html         # Main HTML page
│   ├── style.css          # CSS styles
│   └── script.js          # JavaScript with EventSource
└── .env                   # Environment variables (create this)
```

## 🔌 API Endpoints

### Health Check
```http
GET /health
```
Returns service status.

### Mood Analysis
```http
POST /mood
Content-Type: application/json

{
    "text": "I'm so excited about the concert!"
}
```

### Server-Sent Events
```http
GET /stream
```
Real-time stream of analyzed messages and music recommendations.

### Static Files
```http
GET /
GET /static/style.css
GET /static/script.js
```

## 🎯 Use Cases

- **Live Streaming Platforms**: Real-time mood analysis for chat moderation
- **Music Streaming Services**: Dynamic playlist generation based on user sentiment
- **Social Media Analytics**: Sentiment analysis of user-generated content
- **Event Management**: Mood-based music selection for live events
- **Customer Support**: Sentiment analysis for customer feedback

## 🛠️ Development

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest
```

### Code Style
```bash
# Install formatting tools
pip install black flake8

# Format code
black .

# Check code style
flake8 .
```

### Docker Support
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8002

CMD ["python", "-c", "import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8002)"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the modern web framework
- [Confluent Kafka](https://www.confluent.io/) for streaming platform
- [TextBlob](https://textblob.readthedocs.io/) for sentiment analysis
- [TextBlob](https://textblob.readthedocs.io/) for natural language processing

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-dj-streamer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-dj-streamer/discussions)
- **Email**: your.email@example.com

---

⭐ **Star this repository if you found it helpful!** 