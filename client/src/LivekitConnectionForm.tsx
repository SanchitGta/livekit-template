import { useState, useEffect } from 'react';
import { Room, ConnectionState } from 'livekit-client';
import { RoomAudioRenderer, RoomContext } from '@livekit/components-react';
import { Loader2, Mic, MicOff, PhoneOff } from 'lucide-react';

interface LivekitConnectionFormProps {
  onRoomReady?: (disconnectFn: () => Promise<void>) => void;
}

export default function LivekitConnectionForm({ onRoomReady }: LivekitConnectionFormProps) {
  // Get stored values from localStorage
  const [wsURL, setWsURL] = useState<string>(() => localStorage.getItem('livekit-wsURL') || '');
  const [token, setToken] = useState<string>(() => localStorage.getItem('livekit-token') || '');
  const [room, setRoom] = useState<Room | null>(null);
  const [isConnecting, setIsConnecting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isMuted, setIsMuted] = useState(false);
  const [transcripts] = useState<{text: string, isFinal: boolean}[]>([]);

  // Save values to localStorage when they change
  useEffect(() => {
    if (wsURL) localStorage.setItem('livekit-wsURL', wsURL);
  }, [wsURL]);

  useEffect(() => {
    if (token) localStorage.setItem('livekit-token', token);
  }, [token]);

  const handleConnect = async () => {
    if (!wsURL || !token) {
      setError('Please provide both URL and token');
      return;
    }

    setError(null);
    setIsConnecting(true);

    try {
      const newRoom = new Room();
      
      // Set up event listeners
      newRoom.on('disconnected', () => {
        setRoom(null);
      });

      // Connect to room
      await newRoom.connect(wsURL, token, {
        autoSubscribe: true
      });

      setRoom(newRoom);
      
      // Call the onRoomReady callback if provided
      if (onRoomReady) {
        const disconnectFn = async () => {
          await newRoom.disconnect();
          setRoom(null);
        };
        
        onRoomReady(disconnectFn);
      }
    } catch (err) {
      console.error('Failed to connect to room:', err);
      setError(`Failed to connect: ${err instanceof Error ? err.message : String(err)}`);
    } finally {
      setIsConnecting(false);
    }
  };

  const handleDisconnect = async () => {
    if (room) {
      await room.disconnect();
      setRoom(null);
    }
  };

  const handleToggleMute = () => {
    if (room) {
      const localParticipant = room.localParticipant;
      const newMuteState = !isMuted;
      localParticipant.setMicrophoneEnabled(!newMuteState);
      setIsMuted(newMuteState);
    }
  };

  // Connected view with controls
  const ConnectedView = () => (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between items-center mb-6">
        <div className="flex items-center">
          <div className={`w-3 h-3 rounded-full ${room?.state === ConnectionState.Connected ? 'bg-green-500' : 'bg-yellow-500'} mr-2`}></div>
          <span className="text-gray-700 font-medium">{room?.state === ConnectionState.Connected ? 'Connected' : 'Connecting'}</span>
        </div>
        <div className="flex space-x-2">
          <button 
            onClick={handleToggleMute}
            className={`p-2 rounded-full ${isMuted ? 'bg-red-100 text-red-600' : 'bg-gray-100 text-gray-600'} hover:bg-opacity-80`}
            title={isMuted ? "Unmute" : "Mute"}
          >
            {isMuted ? <MicOff size={20} /> : <Mic size={20} />}
          </button>
          <button 
            onClick={handleDisconnect}
            className="p-2 rounded-full bg-red-100 text-red-600 hover:bg-opacity-80"
            title="End Call"
          >
            <PhoneOff size={20} />
          </button>
        </div>
      </div>
      
      <div className="mb-4">
        <h3 className="text-sm font-medium text-gray-500 mb-2">Agent State</h3>
        <div className="bg-gray-50 p-3 rounded-md">
          <span className="text-gray-800">Ready</span>
        </div>
      </div>
      
      <div>
        <h3 className="text-sm font-medium text-gray-500 mb-2">Transcripts</h3>
        <div className="bg-gray-50 p-3 rounded-md h-40 overflow-y-auto">
          {transcripts.length > 0 ? (
            transcripts.map((transcript, index) => (
              <div key={index} className={`mb-2 ${transcript.isFinal ? 'text-gray-800' : 'text-gray-500 italic'}`}>
                {transcript.text}
              </div>
            ))
          ) : (
            <div className="text-gray-400 text-center py-4">No transcripts available</div>
          )}
        </div>
      </div>
    </div>
  );

  return (
    <div className="w-full">
      {room ? (
        <RoomContext.Provider value={room}>
          <RoomAudioRenderer />
          <ConnectedView />
        </RoomContext.Provider>
      ) : (
        <div className="bg-white rounded-lg shadow p-6">
          <div className="mb-4">
            <label htmlFor="wsURL" className="block text-sm font-medium text-gray-700 mb-1">Server URL</label>
            <input 
              type="text" 
              id="wsURL" 
              value={wsURL} 
              onChange={(e) => setWsURL(e.target.value)}
              placeholder="Enter WebSocket URL"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          
          <div className="mb-6">
            <label htmlFor="token" className="block text-sm font-medium text-gray-700 mb-1">Token</label>
            <input 
              type="text" 
              id="token" 
              value={token} 
              onChange={(e) => setToken(e.target.value)}
              placeholder="Enter your token"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          
          {error && (
            <div className="mb-4 p-3 bg-red-50 text-red-700 rounded-md text-sm">
              {error}
            </div>
          )}
          
          <button 
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
            onClick={handleConnect}
            disabled={isConnecting}
          >
            {isConnecting ? (
              <div className="flex items-center justify-center">
                <Loader2 className="animate-spin mr-2" size={18} />
                <span>Connecting...</span>
              </div>
            ) : 'Connect'}
          </button>
        </div>
      )}
    </div>
  );
}
