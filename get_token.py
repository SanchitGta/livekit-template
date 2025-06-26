# server.py
import os
import uuid
from livekit import api

from dotenv import load_dotenv
load_dotenv()

def getToken(identity, name, room):
  token = api.AccessToken(os.getenv('LIVEKIT_API_KEY'), os.getenv('LIVEKIT_API_SECRET')) \
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

