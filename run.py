#!/usr/bin/env python
"""
Swiggy Chatbot - Main Runner Script
"""

import os
import sys
import subprocess
import time
from colorama import init, Fore, Back, Style
init()

def print_banner():
    """Print startup banner"""
    banner = """
    ╔═══════════════════════════════════════════╗
    ║      🍔 SWIGGY AI CHATBOT v2.0 🍔        ║
    ║         Powered by Mistral AI             ║
    ╚═══════════════════════════════════════════╝
    """
    print(Fore.YELLOW + banner + Style.RESET_ALL)

def check_requirements():
    """Check if all requirements are installed"""
    print(f"\n{Fore.CYAN}Checking requirements...{Style.RESET_ALL}")
    
    required_packages = [
        'llama_cpp',
        'fastapi',
        'uvicorn',
        'pydantic'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"{Fore.GREEN}✅ {package}{Style.RESET_ALL}")
        except ImportError:
            print(f"{Fore.RED}❌ {package} - Not installed{Style.RESET_ALL}")
            missing.append(package)
    
    if missing:
        print(f"\n{Fore.YELLOW}Install missing packages:{Style.RESET_ALL}")
        print(f"pip install -r requirements.txt")
        return False
    
    return True

def check_model():
    """Check if model file exists"""
    print(f"\n{Fore.CYAN}Checking model...{Style.RESET_ALL}")
    
    model_path = "./models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
    
    if os.path.exists(model_path):
        size = os.path.getsize(model_path) / (1024**3)  # Convert to GB
        print(f"{Fore.GREEN}✅ Model found ({size:.2f} GB){Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.RED}❌ Model not found{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Download the model:{Style.RESET_ALL}")
        print("1. Go to: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF")
        print("2. Download: mistral-7b-instruct-v0.2.Q4_K_M.gguf")
        print("3. Place in: ./models/ folder")
        return False

def check_data_files():
    """Check if data files exist"""
    print(f"\n{Fore.CYAN}Checking data files...{Style.RESET_ALL}")
    
    data_files = [
        "data/restaurants.json",
        "data/orders.json",
        "data/menu.json",
        "data/conversations.json"
    ]
    
    all_exist = True
    for file in data_files:
        if os.path.exists(file):
            print(f"{Fore.GREEN}✅ {file}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ {file} - Missing{Style.RESET_ALL}")
            all_exist = False
    
    if not all_exist:
        print(f"\n{Fore.YELLOW}Create missing data files from Step 2.3{Style.RESET_ALL}")
        return False
    
    return True

def start_server():
    """Start the FastAPI server"""
    print(f"\n{Fore.GREEN}Starting Swiggy Chatbot Server...{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Server URL: http://localhost:8000{Style.RESET_ALL}")
    print(f"{Fore.CYAN}API Docs: http://localhost:8000/docs{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Frontend: Open frontend/index.html in browser{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}Press Ctrl+C to stop the server{Style.RESET_ALL}\n")
    
    try:
        subprocess.run(["python", "app.py"])
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Server stopped by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

def main():
    """Main runner function"""
    print_banner()
    
    # Check everything
    checks = [
        ("Requirements", check_requirements),
        ("Model", check_model),
        ("Data Files", check_data_files)
    ]
    
    all_passed = True
    for name, check_func in checks:
        if not check_func():
            all_passed = False
    
    if not all_passed:
        print(f"\n{Fore.RED}⚠️ Some checks failed. Please fix the issues above.{Style.RESET_ALL}")
        sys.exit(1)
    
    print(f"\n{Fore.GREEN}✅ All checks passed!{Style.RESET_ALL}")
    
    # Show options
    print(f"\n{Fore.CYAN}What would you like to do?{Style.RESET_ALL}")
    print("1. Start Chatbot Server")
    print("2. Run Tests")
    print("3. View Analytics")
    print("4. Exit")
    
    choice = input(f"\n{Fore.YELLOW}Enter choice (1-4): {Style.RESET_ALL}")
    
    if choice == "1":
        start_server()
    elif choice == "2":
        print(f"\n{Fore.CYAN}Running tests...{Style.RESET_ALL}")
        subprocess.run(["python", "test_chatbot.py"])
    elif choice == "3":
        print(f"\n{Fore.CYAN}Generating analytics...{Style.RESET_ALL}")
        subprocess.run(["python", "analytics.py"])
    elif choice == "4":
        print(f"{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
        sys.exit(0)
    else:
        print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")

if __name__ == "__main__":
    main()