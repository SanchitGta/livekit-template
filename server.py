import os
import json
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import uuid

from utils.settings import load_settings
from get_token import getToken

app = Flask(__name__, static_folder='client/dist')
CORS(app)

@app.route('/api/settings')
def get_settings():
    """Return settings to the client (excluding sensitive data)"""
    settings = load_settings()
    
    # Validate LiveKit URLs
    livekit_ws_url = settings["livekit"]["ws_url"]
    livekit_url = settings["livekit"]["url"]
    
    # Ensure URLs are properly formatted
    if not livekit_ws_url or not livekit_ws_url.startswith("wss://"):
        print(f"WARNING: Invalid LiveKit WebSocket URL: {livekit_ws_url}")
    
    if not livekit_url or not livekit_url.startswith("wss://"):
        print(f"WARNING: Invalid LiveKit URL: {livekit_url}")
    
    # Create a copy of settings without sensitive information
    client_settings = {
        "client": settings["client"],
        "livekit": {
            "ws_url": livekit_ws_url,
            "url": livekit_url
        },
        "agent": settings["agent"]
    }
    
    print(f"Sending settings to client: {json.dumps(client_settings['livekit'])}")
    return jsonify(client_settings)

@app.route('/api/token')
def get_token():
    """Generate and return a token for LiveKit"""
    settings = load_settings()
    room_name = f"session_{str(uuid.uuid4())[:6]}"
    token = getToken("user", "User Name", room_name)
    
    return jsonify({
        "token": token,
        "roomName": room_name
    })

# Serve the React app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    settings = load_settings()
    port = settings["deployment"]["backend"]["port"]
    app.run(host='0.0.0.0', port=port)
