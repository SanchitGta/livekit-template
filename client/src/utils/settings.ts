// settings.ts - Client-side settings utility

interface AgentSTT {
  provider: string;
  model: string;
  language: string;
}

interface AgentLLM {
  provider: string;
  model: string;
}

interface AgentTTS {
  provider: string;
}

interface AgentVAD {
  provider: string;
}

interface AgentTurnDetection {
  provider: string;
}

interface AgentNoiseCancellation {
  provider: string;
}

interface Agent {
  instructions: string;
  greeting: string;
  stt: AgentSTT;
  llm: AgentLLM;
  tts: AgentTTS;
  vad: AgentVAD;
  turn_detection: AgentTurnDetection;
  noise_cancellation: AgentNoiseCancellation;
}

interface Livekit {
  url: string;
  api_key: string;
  api_secret: string;
  ws_url: string;
}

interface Client {
  title: string;
  auto_connect: boolean;
}

interface Settings {
  api_keys: {
    deepgram: string;
    openai: string;
  };
  api_urls: {
    openai_base_url: string;
  };
  livekit: Livekit;
  agent: Agent;
  client: Client;
  deployment: {
    backend: {
      port: number;
    };
    client: {
      port: number;
    };
  };
}

// Function to fetch settings from the server
export async function fetchSettings(): Promise<Settings> {
  try {
    console.log('Fetching settings from server...');
    const response = await fetch('/api/settings');
    if (!response.ok) {
      throw new Error(`Failed to fetch settings: ${response.statusText}`);
    }
    const data = await response.json();
    console.log('Received settings from server:', data);
    
    // Validate LiveKit URLs
    if (!data.livekit || !data.livekit.ws_url) {
      console.error('Missing LiveKit WebSocket URL in server response');
    } else {
      console.log('LiveKit WebSocket URL:', data.livekit.ws_url);
    }
    
    return data;
  } catch (error) {
    console.error('Error fetching settings:', error);
    throw error;
  }
}

// Create a simple settings cache
let settingsCache: Settings | null = null;

// Get settings (from cache if available)
export async function getSettings(): Promise<Settings> {
  if (settingsCache) {
    return settingsCache;
  }
  
  settingsCache = await fetchSettings();
  return settingsCache;
}

// Get token from the server
export async function getToken(): Promise<{ token: string; roomName: string }> {
  try {
    const response = await fetch('/api/token');
    if (!response.ok) {
      throw new Error(`Failed to fetch token: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching token:', error);
    throw error;
  }
}
