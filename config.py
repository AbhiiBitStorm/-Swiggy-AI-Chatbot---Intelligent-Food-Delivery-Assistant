import os
from typing import Dict, Any

class Config:
    """Chatbot Configuration"""
    
    # Server Settings
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    DEBUG = True
    
    # Model Settings
    MODEL_PATH = "./models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
    MODEL_PARAMS = {
        "n_ctx": 4096,
        "n_threads": 8,
        "n_gpu_layers": 0,  # Set to 20+ for GPU
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 256
    }
    
    # Data Settings
    DATA_DIR = "data"
    DATA_FILES = {
        "restaurants": "restaurants.json",
        "orders": "orders.json",
        "menu": "menu.json",
        "conversations": "conversations.json"
    }
    
    # Chat Settings
    MAX_HISTORY_LENGTH = 20
    SESSION_TIMEOUT = 3600  # 1 hour
    
    # Response Templates
    WELCOME_MESSAGE = """👋 Welcome to Swiggy Support! I'm your AI assistant.
    
I can help you with:
• 📦 Order tracking (provide order ID)
• 🍴 Restaurant discovery
• 📋 Menu browsing
• ⚡ Quick delivery options
• ⭐ Popular recommendations

How can I assist you today?"""
    
    ERROR_MESSAGES = {
        "order_not_found": "❌ Order {} not found. Please check the order ID.",
        "restaurant_not_found": "❌ Restaurant not found. Try searching differently.",
        "server_error": "❌ Sorry, I encountered an error. Please try again.",
        "invalid_input": "❌ I didn't understand that. Can you please rephrase?"
    }
    
    # Feature Flags
    FEATURES = {
        "hindi_support": True,
        "voice_input": False,
        "sentiment_analysis": False,
        "recommendation_engine": True,
        "auto_complete": True
    }
    
    @classmethod
    def get_data_path(cls, file_type: str) -> str:
        """Get full path for data file"""
        return os.path.join(cls.DATA_DIR, cls.DATA_FILES.get(file_type, ""))
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration"""
        # Check if model exists
        if not os.path.exists(cls.MODEL_PATH):
            print(f"⚠️ Model not found at: {cls.MODEL_PATH}")
            print("Download from: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF")
            return False
        
        # Check if data directory exists
        if not os.path.exists(cls.DATA_DIR):
            os.makedirs(cls.DATA_DIR)
            print(f"📁 Created data directory: {cls.DATA_DIR}")
        
        # Check data files
        for file_type, filename in cls.DATA_FILES.items():
            path = cls.get_data_path(file_type)
            if not os.path.exists(path):
                print(f"⚠️ Missing data file: {path}")
                if file_type == "conversations":
                    # Create empty conversations file
                    import json
                    with open(path, 'w') as f:
                        json.dump({"conversations": []}, f)
                    print(f"✅ Created empty {filename}")
        
        return True
    
    @classmethod
    def display_config(cls):
        """Display current configuration"""
        print("\n" + "="*50)
        print(" CHATBOT CONFIGURATION")
        print("="*50)
        print(f"Server: http://{cls.API_HOST}:{cls.API_PORT}")
        print(f"Model: {os.path.basename(cls.MODEL_PATH)}")
        print(f"Data Directory: {cls.DATA_DIR}")
        print("\nFeatures:")
        for feature, enabled in cls.FEATURES.items():
            status = "✅" if enabled else "❌"
            print(f"  {status} {feature.replace('_', ' ').title()}")
        print("="*50)

# Validate on import
if __name__ == "__main__":
    Config.display_config()
    Config.validate_config()