#!/bin/bash
source venv/bin/activate

# Start the server in the background
python server.py &
server_pid=$!

# Wait a moment for the server to initialize
sleep 2

# Start the agent with dev environment
python agent.py dev &
agent_pid=$!

# Function to handle script termination
cleanup() {
  echo "Stopping server and agent..."
  kill $server_pid $agent_pid 2>/dev/null
  exit 0
}

# Set up trap to catch termination signals
trap cleanup SIGINT SIGTERM

# Keep the script running
echo "Server and agent are running. Press Ctrl+C to stop."
wait
