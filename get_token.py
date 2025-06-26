# server.py
import os
import uuid
import json
from livekit import api

from utils.settings import load_settings

def getToken(identity, name, room):
  settings = load_settings()
  livekit_settings = settings['livekit']
  
  token = api.AccessToken(livekit_settings['api_key'], livekit_settings['api_secret']) \
    .with_identity(identity) \
    .with_name(name) \
    .with_grants(api.VideoGrants(
        room_join=True,
        room=room,
    ))
  return token.to_jwt()

if __name__ == "__main__":
  room_name = f"session_{str(uuid.uuid4())[:6]}"
  token = getToken("user", "User Name", room_name)
  print("\n\nToken:", room_name)
  print(token)
  print("\n\nRoom Name:", room_name)
  print(room_name)

