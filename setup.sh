#!/bin/bash

# LiveKit Voice Chat Application Setup Script
# This script automates the setup of the LiveKit Voice Chat application

# Text formatting
BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
BLUE="\033[0;34m"
RED="\033[0;31m"
NC="\033[0m" # No Color

# Print section header
print_header() {
  echo -e "\n${BOLD}${BLUE}=== $1 ===${NC}\n"
}

# Print success message
print_success() {
  echo -e "${GREEN}✓ $1${NC}"
}

# Print info message
print_info() {
  echo -e "${YELLOW}➜ $1${NC}"
}

# Print error message and exit
print_error() {
  echo -e "${RED}✗ $1${NC}"
  exit 1
}

# Check if a command exists
command_exists() {
  command -v "$1" &> /dev/null
}

# Check required tools
check_requirements() {
  print_header "Checking Requirements"
  
  # Check for git
  if ! command_exists git; then
    print_error "Git is not installed. Please install git and try again."
  fi
  print_success "Git is installed"
  
  # Check for python
  if ! command_exists python3; then
    print_error "Python 3 is not installed. Please install Python 3 and try again."
  fi
  print_success "Python 3 is installed"
  
  # Check for pip
  if ! command_exists pip3; then
    print_error "pip3 is not installed. Please install pip3 and try again."
  fi
  print_success "pip3 is installed"
  
  # Check for node
  if ! command_exists node; then
    print_error "Node.js is not installed. Please install Node.js and try again."
  fi
  print_success "Node.js is installed"
  
  # Check for npm
  if ! command_exists npm; then
    print_error "npm is not installed. Please install npm and try again."
  fi
  print_success "npm is installed"
}

# Clone the repository if not already in it
clone_repository() {
  print_header "Setting Up Repository"
  
  # Check if we're already in the repository
  if [ -d ".git" ] && [ -f "settings.json" ]; then
    print_info "Already in the repository directory"
    return
  fi
  
  # Ask for repository URL if not already in the repository
  read -p "Enter the repository URL (or press Enter to skip if already cloned): " repo_url
  
  if [ -n "$repo_url" ]; then
    print_info "Cloning repository from $repo_url"
    git clone "$repo_url" livekit-voice-chat || print_error "Failed to clone repository"
    cd livekit-voice-chat || print_error "Failed to enter repository directory"
    print_success "Repository cloned successfully"
  else
    print_info "Skipping repository clone"
  fi
}

# Setup Python backend
setup_backend() {
  print_header "Setting Up Backend"
  
  # Create virtual environment if it doesn't exist
  if [ ! -d "venv" ]; then
    print_info "Creating virtual environment"
    python3 -m venv venv || print_error "Failed to create virtual environment"
    print_success "Virtual environment created"
  else
    print_info "Virtual environment already exists"
  fi
  
  # Activate virtual environment
  print_info "Activating virtual environment"
  source venv/bin/activate || print_error "Failed to activate virtual environment"
  
  # Install dependencies
  print_info "Installing Python dependencies"
  pip install -r requirements.txt || print_error "Failed to install Python dependencies"
  pip install flask flask-cors || print_error "Failed to install Flask dependencies"
  print_success "Python dependencies installed"
}

# Setup React frontend
setup_frontend() {
  print_header "Setting Up Frontend"
  
  # Check if client directory exists
  if [ ! -d "client" ]; then
    print_error "Client directory not found"
  fi
  
  # Install dependencies
  print_info "Installing frontend dependencies"
  cd client || print_error "Failed to enter client directory"
  npm install || print_error "Failed to install frontend dependencies"
  
  # Build frontend
  print_info "Building frontend"
  npm run build || print_error "Failed to build frontend"
  print_success "Frontend built successfully"
  
  # Return to root directory
  cd ..
}

# Configure application settings
configure_settings() {
  print_header "Configuring Application"
  
  # Check if settings.json exists
  if [ ! -f "settings.json" ]; then
    print_error "settings.json not found"
  fi
  
  # Ask if user wants to modify settings
  read -p "Do you want to modify the application settings? (y/n): " modify_settings
  
  if [ "$modify_settings" = "y" ] || [ "$modify_settings" = "Y" ]; then
    # Open settings.json in default editor
    print_info "Opening settings.json in editor"
    if command_exists nano; then
      nano settings.json
    elif command_exists vim; then
      vim settings.json
    elif command_exists vi; then
      vi settings.json
    else
      print_error "No suitable text editor found (nano, vim, vi)"
    fi
    print_success "Settings updated"
  else
    print_info "Using default settings"
  fi
}

# Start the application
start_application() {
  print_header "Starting Application"
  
  # Ask if user wants to start the application
  read -p "Do you want to start the application now? (y/n): " start_app
  
  if [ "$start_app" = "y" ] || [ "$start_app" = "Y" ]; then
    print_info "Starting backend server"
    # Start backend server in the background
    source venv/bin/activate
    python server.py &
    backend_pid=$!
    print_success "Backend server started (PID: $backend_pid)"
    
    # Wait for server to start
    sleep 2
    
    # Open browser
    print_info "Opening application in browser"
    if command_exists xdg-open; then
      xdg-open http://localhost:8000
    elif command_exists open; then
      open http://localhost:8000
    else
      print_info "Please open http://localhost:8000 in your browser"
    fi
    
    # Wait for user to exit
    read -p "Press Enter to stop the application..." 
    
    # Stop backend server
    kill $backend_pid
    print_success "Application stopped"
  else
    print_info "To start the application later, run: ./start.sh"
  fi
}

# Main function
main() {
  print_header "LiveKit Voice Chat Setup"
  
  check_requirements
  clone_repository
  setup_backend
  setup_frontend
  configure_settings
  
  # Create start script
  cat > start.sh << 'EOL'
#!/bin/bash
source venv/bin/activate
python server.py
EOL
  chmod +x start.sh
  print_success "Created start.sh script"
  
  start_application
  
  print_header "Setup Complete"
  print_info "You can start the application anytime by running: ./start.sh"
}

# Run main function
main
