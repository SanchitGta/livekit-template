import '@livekit/components-styles';
import LivekitConnectionForm from './LivekitConnectionForm';

function App() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <div className="w-full max-w-md">
        <h1 className="text-2xl font-bold text-center mb-6 text-gray-800">LiveKit Voice Chat</h1>
        <LivekitConnectionForm />
      </div>
    </div>
  );
}

export default App;
