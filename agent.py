import os
import logging
import json

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    openai,
    deepgram,
    noise_cancellation,
    silero,
)

# from livekit.plugins.turn_detector.multilingual import MultilingualModel
from livekit.plugins.turn_detector.english import EnglishModel

from utils.settings import load_settings

# Load settings from settings.json
settings = load_settings()


# Logger setup (insert once at top of each module)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s.%(msecs)03d – %(levelname)s – %(name)s – %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)



class Assistant(Agent):
    def __init__(self) -> None:
        agent_settings = settings['agent']
        super().__init__(instructions=agent_settings['instructions'])


async def entrypoint(ctx: agents.JobContext):
    logger.info(f"Entering entrypoint with room={getattr(ctx.room, 'name', None)}")
    
    # Configure OpenAI client with custom settings
    logger.info("Printing context")
    print("namaste_ctx: ", ctx)

    logger.info("Initializing AgentSession")
    agent_settings = settings['agent']
    stt_settings = agent_settings['stt']
    llm_settings = agent_settings['llm']
    
    session = AgentSession(
        stt=deepgram.STT(model=stt_settings['model'], language=stt_settings['language']),
        llm=openai.LLM(model=llm_settings['model']),
        tts=deepgram.TTS(),
        vad=silero.VAD.load(),
        turn_detection=EnglishModel(),
        # turn_detection=MultilingualModel(),
    )
    logger.info("AgentSession initialized")

    logger.info("Starting session")
    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(), 
        ),
    )
    logger.info("Session started")

    await ctx.connect()

    await session.generate_reply(
        instructions=agent_settings['greeting']
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))