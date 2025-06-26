#!/usr/bin/env python3
"""
Test script for LiveKit Voice Chat application setup
This script verifies that all components are properly configured
"""

import os
import json
import sys
import subprocess
from pathlib import Path

# Text formatting for console output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(message):
    """Print a formatted header message"""
    print(f"\n{Colors.BOLD}=== {message} ==={Colors.END}\n")

def print_success(message):
    """Print a success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_warning(message):
    """Print a warning message"""
    print(f"{Colors.YELLOW}! {message}{Colors.END}")

def print_error(message):
    """Print an error message"""
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def check_file_exists(path, description):
    """Check if a file exists and print the result"""
    if os.path.exists(path):
        print_success(f"{description} found at {path}")
        return True
    else:
        print_error(f"{description} not found at {path}")
        return False

def check_directory_exists(path, description):
    """Check if a directory exists and print the result"""
    if os.path.isdir(path):
        print_success(f"{description} found at {path}")
        return True
    else:
        print_error(f"{description} not found at {path}")
        return False

def check_settings_file():
    """Validate the settings.json file"""
    settings_path = Path("settings.json")
    
    if not check_file_exists(settings_path, "Settings file"):
        return False
    
    try:
        with open(settings_path, 'r') as f:
            settings = json.load(f)
            
        # Check required sections
        required_sections = ["api_keys", "livekit", "agent", "client", "deployment"]
        missing_sections = [section for section in required_sections if section not in settings]
        
        if missing_sections:
            print_error(f"Missing sections in settings.json: {', '.join(missing_sections)}")
            return False
        
        # Check API keys
        if not settings["api_keys"].get("deepgram"):
            print_warning("Deepgram API key is not set in settings.json")
        
        if not settings["api_keys"].get("openai"):
            print_warning("OpenAI API key is not set in settings.json")
        
        # Check LiveKit settings
        livekit_settings = settings.get("livekit", {})
        if not all(key in livekit_settings for key in ["url", "api_key", "api_secret", "ws_url"]):
            print_warning("LiveKit settings are incomplete in settings.json")
        
        print_success("Settings file validation passed")
        return True
        
    except json.JSONDecodeError:
        print_error("settings.json is not valid JSON")
        return False
    except Exception as e:
        print_error(f"Error validating settings.json: {str(e)}")
        return False

def check_backend_setup():
    """Check backend setup"""
    print_header("Checking Backend Setup")
    
    # Check required files
    backend_files = [
        ("agent.py", "Agent implementation"),
        ("get_token.py", "Token generation utility"),
        ("server.py", "Flask server"),
        ("requirements.txt", "Python dependencies")
    ]
    
    all_files_exist = True
    for file_path, description in backend_files:
        if not check_file_exists(file_path, description):
            all_files_exist = False
    
    # Check utils directory and settings module
    utils_dir = "utils"
    if not check_directory_exists(utils_dir, "Utils directory"):
        return False
    
    if not check_file_exists(os.path.join(utils_dir, "settings.py"), "Settings utility"):
        return False
    
    if not check_file_exists(os.path.join(utils_dir, "__init__.py"), "Utils package init file"):
        print_warning("Utils package __init__.py file not found")
    
    return all_files_exist

def check_frontend_setup():
    """Check frontend setup"""
    print_header("Checking Frontend Setup")
    
    # Check client directory
    client_dir = "client"
    if not check_directory_exists(client_dir, "Client directory"):
        return False
    
    # Check package.json
    if not check_file_exists(os.path.join(client_dir, "package.json"), "Frontend package.json"):
        return False
    
    # Check source files
    src_dir = os.path.join(client_dir, "src")
    if not check_directory_exists(src_dir, "Frontend source directory"):
        return False
    
    frontend_files = [
        ("App.tsx", "Main App component"),
        ("LivekitConnectionForm.tsx", "LiveKit connection form component"),
        (os.path.join("utils", "settings.ts"), "Frontend settings utility")
    ]
    
    all_files_exist = True
    for file_path, description in frontend_files:
        full_path = os.path.join(src_dir, file_path)
        if not check_file_exists(full_path, description):
            all_files_exist = False
    
    return all_files_exist

def check_scripts():
    """Check setup and start scripts"""
    print_header("Checking Scripts")
    
    scripts = [
        ("setup.sh", "Setup script"),
        ("start.sh", "Start script")
    ]
    
    all_scripts_exist = True
    for script_path, description in scripts:
        if not check_file_exists(script_path, description):
            all_scripts_exist = False
            continue
        
        # Check if scripts are executable
        if not os.access(script_path, os.X_OK):
            print_warning(f"{description} is not executable. Run: chmod +x {script_path}")
    
    return all_scripts_exist

def main():
    """Main function to run all checks"""
    print_header("LiveKit Voice Chat Setup Test")
    
    # Run all checks
    settings_ok = check_settings_file()
    backend_ok = check_backend_setup()
    frontend_ok = check_frontend_setup()
    scripts_ok = check_scripts()
    
    # Print summary
    print_header("Test Summary")
    
    if all([settings_ok, backend_ok, frontend_ok, scripts_ok]):
        print_success("All checks passed! The application is properly set up.")
        print("\nYou can start the application by running:")
        print("\n    ./start.sh\n")
        return 0
    else:
        print_error("Some checks failed. Please fix the issues before running the application.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
