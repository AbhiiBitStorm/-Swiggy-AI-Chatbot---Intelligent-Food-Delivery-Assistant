import json
import os
from typing import List, Dict, Optional
from datetime import datetime

class DataManager:
    def __init__(self):
        self.data_dir = "data"
        self.ensure_data_files()
        self.load_all_data()
    
    def ensure_data_files(self):
        """Ensure all data files exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # Create empty conversations file if not exists
        conv_file = os.path.join(self.data_dir, "conversations.json")
        if not os.path.exists(conv_file):
            with open(conv_file, 'w') as f:
                json.dump({"conversations": []}, f)
    
    def load_all_data(self):
        """Load all data into memory"""
        # Load restaurants
        with open(os.path.join(self.data_dir, "restaurants.json"), 'r', encoding='utf-8') as f:
            self.restaurants_data = json.load(f)
        
        # Load menu
        with open(os.path.join(self.data_dir, "menu.json"), 'r', encoding='utf-8') as f:
            self.menu_data = json.load(f)
        
        # Load orders
        with open(os.path.join(self.data_dir, "orders.json"), 'r', encoding='utf-8') as f:
            self.orders_data = json.load(f)
        
        # Load conversations
        with open(os.path.join(self.data_dir, "conversations.json"), 'r', encoding='utf-8') as f:
            self.conversations_data = json.load(f)
    
    def search_restaurants(self, query: str) -> List[Dict]:
        """Search restaurants by name or cuisine"""
        query = query.lower()
        results = []
        
        for restaurant in self.restaurants_data['restaurants']:
            if (query in restaurant['name'].lower() or 
                query in restaurant['cuisine'].lower()):
                results.append(restaurant)
        
        return results[:5]  # Return top 5 results
    
    def get_order_status(self, order_id: str) -> Optional[Dict]:
        """Get order status by order ID"""
        for order in self.orders_data['orders']:
            if order['order_id'] == order_id.upper():
                return order
        return None
    
    def get_restaurant_menu(self, restaurant_id: str) -> List[Dict]:
        """Get menu items for a restaurant"""
        for menu in self.menu_data['menu_items']:
            if menu['restaurant_id'] == restaurant_id:
                return menu['items']
        return []
    
    def get_restaurant_by_name(self, name: str) -> Optional[Dict]:
        """Get restaurant details by name"""
        for restaurant in self.restaurants_data['restaurants']:
            if name.lower() in restaurant['name'].lower():
                return restaurant
        return None
    
    def save_conversation(self, session_id: str, user_msg: str, bot_response: str):
        """Save conversation to file"""
        conversation = {
            "session_id": session_id,
            "user_message": user_msg,
            "bot_response": bot_response,
            "timestamp": datetime.now().isoformat()
        }
        
        self.conversations_data['conversations'].append(conversation)
        
        # Save to file
        with open(os.path.join(self.data_dir, "conversations.json"), 'w', encoding='utf-8') as f:
            json.dump(self.conversations_data, f, indent=2, ensure_ascii=False)
    
    def get_conversation_history(self, session_id: str) -> List[Dict]:
        """Get chat history for a session"""
        history = []
        for conv in self.conversations_data['conversations']:
            if conv['session_id'] == session_id:
                history.append(conv)
        return history[-10:]  # Return last 10 messages
    
    def get_popular_restaurants(self) -> List[Dict]:
        """Get popular restaurants (rating > 4.3)"""
        popular = []
        for restaurant in self.restaurants_data['restaurants']:
            if restaurant['rating'] >= 4.3:
                popular.append(restaurant)
        return sorted(popular, key=lambda x: x['rating'], reverse=True)[:3]
    
    def get_quick_delivery_restaurants(self) -> List[Dict]:
        """Get restaurants with quick delivery (< 30 mins)"""
        quick = []
        for restaurant in self.restaurants_data['restaurants']:
            delivery_time = int(restaurant['delivery_time'].split()[0])
            if delivery_time <= 30:
                quick.append(restaurant)
        return quick

# Create global instance
data_manager = DataManager()