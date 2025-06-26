# LiveKit Voice Chat Application

A modular, configurable voice chat application built with LiveKit, React, and Flask.

## Features

- Voice chat using LiveKit's real-time communication platform
- AI-powered conversational agent using OpenAI and Deepgram
- Fully configurable through a central `settings.json` file
- Single-click connection to the voice chat
- Easy setup with automated scripts

## Quick Start

### Option 1: Using Setup Script

1. Clone this repository
2. Run the setup script:
   ```
   ./setup.sh
   ```
3. The setup script will:
   - Check for required dependencies
   - Set up the Python virtual environment
   - Install backend dependencies
   - Build the frontend
   - Configure application settings
   - Create a start script

4. Start the application:
   ```
   ./start.sh
   ```

### Option 2: Using Docker

1. Clone this repository
2. Make sure Docker and Docker Compose are installed
3. Build and start the application:
   ```
   docker-compose up --build
   ```
   For subsequent runs, you can simply use:
   ```
   docker-compose up
   ```

### Using the Application

1. Open your browser and navigate to `http://localhost:8000`
2. Click the "Connect" button to start a voice chat session

## Configuration

All application settings are stored in `settings.json`. You can modify this file to customize:

- API keys (Deepgram, OpenAI)
- LiveKit server configuration
- Agent settings (instructions, models, etc.)
- Client UI settings
- Deployment configuration

Example `settings.json`:
```json
{
  "api_keys": {
    "deepgram": "your_deepgram_api_key",
    "openai": "your_openai_api_key"
  },
  "api_urls": {
    "openai_base_url": "https://api.openai.com/v1"
  },
  "livekit": {
    "url": "wss://your-livekit-server.cloud",
    "api_key": "your_livekit_api_key",
    "api_secret": "your_livekit_api_secret",
    "ws_url": "wss://your-livekit-server.cloud"
  },
  "agent": {
    "instructions": "You are a helpful voice AI assistant.",
    "greeting": "Greet the user and offer your assistance.",
    "stt": {
      "provider": "deepgram",
      "model": "nova-3",
      "language": "multi"
    },
    "llm": {
      "provider": "openai",
      "model": "gpt-4o-mini"
    },
    "tts": {
      "provider": "deepgram"
    },
    "vad": {
      "provider": "silero"
    },
    "turn_detection": {
      "provider": "english"
    },
    "noise_cancellation": {
      "provider": "bvc"
    }
  },
  "client": {
    "title": "LiveKit Voice Chat",
    "auto_connect": true
  },
  "deployment": {
    "backend": {
      "port": 8000
    },
    "client": {
      "port": 5173
    }
  }
}
```

## Project Structure

```
livekit/
├── agent.py               # Agent implementation
├── client/                # React frontend
│   ├── src/
│   │   ├── App.tsx
│   │   ├── LivekitConnectionForm.tsx
│   │   └── utils/
│   │       └── settings.ts
│   └── ...
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Docker configuration
├── get_token.py           # Token generation utility
├── requirements.txt       # Python dependencies
├── server.py              # Flask server for API endpoints
├── settings.json          # Central configuration file
├── setup.sh               # Setup script
├── start.sh               # Start script
├── test_setup.py          # Setup validation script
└── utils/
    └── settings.py        # Settings utility for backend
```

## Requirements

### For Script Setup
- Python 3.8+
- Node.js 16+
- npm 8+
- Git

### For Docker Setup
- Docker
- Docker Compose

## License

This project is licensed under the MIT License - see the LICENSE file for details.
