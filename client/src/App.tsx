import '@livekit/components-styles';
import { useState, useEffect } from 'react';
import LivekitConnectionForm from './LivekitConnectionForm';
import { getSettings } from './utils/settings';

function App() {
  const [title, setTitle] = useState('LiveKit Voice Chat');
  
  useEffect(() => {
    // Load title from settings
    const loadSettings = async () => {
      try {
        const settings = await getSettings();
        setTitle(settings.client.title);
      } catch (error) {
        console.error('Failed to load settings:', error);
      }
    };
    
    loadSettings();
  }, []);
  
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <div className="w-full max-w-md">
        <h1 className="text-2xl font-bold text-center mb-6 text-gray-800">{title}</h1>
        <LivekitConnectionForm />
      </div>
    </div>
  );
}

export default App;
