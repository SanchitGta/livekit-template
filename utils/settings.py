import json
import os
from pathlib import Path

def load_settings():
    """
    Load settings from settings.json file.
    Returns a dictionary with all settings.
    """
    settings_path = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / "settings.json"
    
    if not settings_path.exists():
        raise FileNotFoundError(f"Settings file not found at {settings_path}")
    
    with open(settings_path, 'r') as f:
        settings = json.load(f)
    
    return settings

def get_env_dict():
    """
    Convert settings to environment variables format for backward compatibility.
    """
    settings = load_settings()
    
    env_dict = {
        "DEEPGRAM_API_KEY": settings["api_keys"]["deepgram"],
        "OPENAI_API_KEY": settings["api_keys"]["openai"],
        "OPENAI_BASE_URL": settings["api_urls"]["openai_base_url"],
        "LIVEKIT_URL": settings["livekit"]["url"],
        "LIVEKIT_API_KEY": settings["livekit"]["api_key"],
        "LIVEKIT_API_SECRET": settings["livekit"]["api_secret"],
        "LIVEKIT_WS_URL": settings["livekit"]["ws_url"]
    }
    
    return env_dict
