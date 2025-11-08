from llama_cpp import Llama
import re
from data_manager import data_manager
from typing import List, Dict, Optional
import time

class SwiggyBot:
    def __init__(self, model_path="./models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"):
        print("🚀 Loading Optimized Mistral model...")
        
        # Optimized model settings for SPEED
        self.llm = Llama(
            model_path=model_path,
            n_ctx=2048,        # Reduced from 4096 (faster)
            n_threads=8,       # Use all CPU cores
            n_batch=512,       # Larger batch for speed
            n_gpu_layers=0,    # Set to 35 if you have GPU
            use_mlock=True,    # Keep in RAM (faster)
            use_mmap=True,     # Memory mapped
            verbose=False      # No debug logs
        )
        
        print("✅ Model loaded (Optimized for Speed)!")
        
        # Response cache for instant replies
        self.response_cache = {}
        
        # Common patterns for instant responses
        self.quick_responses = {
            'hi': "👋 Hello! How can I help you today?",
            'hello': "👋 Hi there! What would you like to know?",
            'help': "I can help you with:\n• 📦 Order tracking\n• 🍴 Restaurant search\n• 📋 Menu viewing\n• 💰 Refunds",
            'thanks': "😊 You're welcome! Anything else I can help with?",
            'thank you': "😊 Happy to help! Let me know if you need anything else.",
            'bye': "👋 Goodbye! Have a great day!",
        }
    
    def check_order_status(self, order_id: str) -> str:
        """INSTANT order status check"""
        order = data_manager.get_order_status(order_id)
        
        if not order:
            return f"❌ Order {order_id} not found. Please check the ID.\n\n📝 Sample IDs: ORD100000, ORD100001, ORD100002"
        
        # Quick status templates
        status_emoji = {
            "preparing": "🍳",
            "out_for_delivery": "🛵",
            "delivered": "✅",
            "cancelled": "❌"
        }
        
        emoji = status_emoji.get(order['status'], '📦')
        
        response = f"{emoji} **Order {order['order_id']}**\n\n"
        response += f"Restaurant: {order['restaurant']}\n"
        response += f"Items: {', '.join(order['items'])}\n"
        response += f"Total: ₹{order['total']}\n"
        response += f"Status: **{order['status'].upper()}**\n"
        
        if order['status'] == 'out_for_delivery':
            response += f"\nDelivery Partner: {order.get('delivery_partner', 'Assigned')}"
            response += f"\n📞 {order.get('partner_phone', 'Updating...')}"
        elif order['status'] == 'delivered':
            response += f"\n✅ Delivered at {order.get('delivery_time', 'Recently')}"
        elif order['status'] == 'preparing':
            response += f"\n⏱️ Expected: {order.get('expected_delivery', '30-40 mins')}"
        elif order['status'] == 'cancelled':
            response += f"\n💰 Refund: {order.get('refund_status', 'Processing')}"
        
        return response
    
    def search_restaurants(self, query: str) -> str:
        """INSTANT restaurant search"""
        results = data_manager.search_restaurants(query)
        
        if not results:
            popular = data_manager.get_popular_restaurants()
            response = f"No exact match for '{query}'. Try these popular ones:\n\n"
            for rest in popular[:3]:
                response += f"🍴 **{rest['name']}**\n   {rest['cuisine']}\n   ⭐ {rest['rating']} | ⏱️ {rest['delivery_time']}\n\n"
            return response
        
        response = f"Found {len(results)} restaurant(s):\n\n"
        for rest in results[:5]:
            response += f"🍴 **{rest['name']}**\n"
            response += f"   📍 {rest['area']}\n"
            response += f"   🍽️ {rest['cuisine']}\n"
            response += f"   ⭐ {rest['rating']} | ⏱️ {rest['delivery_time']} | 💵 ₹{rest['delivery_fee']}\n\n"
        
        return response
    
    def show_menu(self, restaurant_name: str) -> str:
        """INSTANT menu display"""
        restaurant = data_manager.get_restaurant_by_name(restaurant_name)
        
        if not restaurant:
            return f"Restaurant '{restaurant_name}' not found."
        
        menu_items = data_manager.get_restaurant_menu(restaurant['id'])
        
        if not menu_items:
            return f"Menu not available for {restaurant['name']}."
        
        response = f"📋 **{restaurant['name']} Menu**\n\n"
        for item in menu_items:
            veg = "🟢" if item['veg'] else "🔴"
            response += f"{veg} **{item['name']}** - ₹{item['price']}\n"
            response += f"   {item['description']} | ⭐ {item['rating']}\n\n"
        
        return response
    
    def process_intent(self, user_message: str) -> Optional[str]:
        """INSTANT intent-based responses"""
        message_lower = user_message.lower().strip()
        
        # 1. Check quick responses (INSTANT)
        for key, response in self.quick_responses.items():
            if message_lower == key or message_lower.startswith(key):
                return response
        
        # 2. Order tracking (INSTANT)
        order_pattern = r'ORD\d{6}'
        order_match = re.search(order_pattern, user_message.upper())
        
        if order_match:
            return self.check_order_status(order_match.group())
        
        if any(word in message_lower for word in ['track', 'order', 'status', 'where']):
            if 'ORD' in user_message.upper():
                match = re.search(r'ORD\d+', user_message.upper())
                if match:
                    return self.check_order_status(match.group())
            return "Please provide order ID (e.g., ORD100000)\n\n📝 Test IDs:\n• ORD100000 (Delivered)\n• ORD100001 (Preparing)\n• ORD100002 (Out for Delivery)"
        
        # 3. Restaurant search (INSTANT)
        cuisines = ['pizza', 'burger', 'biryani', 'dosa', 'chinese', 'north indian', 'south indian', 'fast food']
        for cuisine in cuisines:
            if cuisine in message_lower:
                return self.search_restaurants(cuisine)
        
        if any(word in message_lower for word in ['restaurant', 'food', 'eat', 'hungry', 'order food']):
            return self.search_restaurants("restaurant")
        
        # 4. Menu (INSTANT)
        if 'menu' in message_lower:
            restaurants = ['domino', 'burger king', 'biryani', 'kfc', 'udupi', 'punjabi']
            for rest_keyword in restaurants:
                if rest_keyword in message_lower:
                    return self.show_menu(rest_keyword)
            return "Which restaurant's menu?\n• Domino's Pizza\n• Burger King\n• Biryani Blues\n• KFC\n• Udupi Garden\n• Punjabi Rasoi"
        
        # 5. Popular/Recommendations (INSTANT)
        if any(word in message_lower for word in ['popular', 'best', 'recommend', 'suggest', 'top']):
            popular = data_manager.get_popular_restaurants()
            response = "🌟 **Top Rated Restaurants:**\n\n"
            for rest in popular:
                response += f"{rest['image']} **{rest['name']}** - ⭐ {rest['rating']}\n"
                response += f"   {rest['cuisine']} | {rest['delivery_time']}\n\n"
            return response
        
        # 6. Quick delivery (INSTANT)
        if any(word in message_lower for word in ['quick', 'fast', 'urgent', 'asap']):
            quick = data_manager.get_quick_delivery_restaurants()
            response = "⚡ **Quick Delivery (Under 30 mins):**\n\n"
            for rest in quick[:3]:
                response += f"{rest['image']} {rest['name']} - {rest['delivery_time']}\n"
            return response
        
        # 7. Refund/Payment (INSTANT)
        if any(word in message_lower for word in ['refund', 'payment', 'money', 'paid', 'charge']):
            return "💰 **Refund Help:**\n\nTo process refund:\n1. Provide order ID\n2. Reason for refund\n3. Refunds take 2-3 business days\n\nNeed help with specific order?"
        
        # 8. Complaint/Issue (INSTANT)
        if any(word in message_lower for word in ['complaint', 'issue', 'problem', 'wrong', 'late', 'cold']):
            return "⚠️ **Report an Issue:**\n\nI'm here to help! Please:\n1. Share your order ID\n2. Describe the issue\n3. I'll connect you with support\n\nOr contact: 1800-1234-5678"
        
        # No instant match found
        return None
    
    def generate_response(self, user_message: str, chat_history: List[Dict] = []) -> str:
        """Generate response - Try instant first, then LLM"""
        
        start_time = time.time()
        
        # Step 1: Try INSTANT response (rules-based)
        instant_response = self.process_intent(user_message)
        if instant_response:
            print(f"⚡ Instant response ({time.time() - start_time:.2f}s)")
            return instant_response
        
        # Step 2: Check cache
        cache_key = user_message.lower().strip()
        if cache_key in self.response_cache:
            print(f"💾 Cached response ({time.time() - start_time:.2f}s)")
            return self.response_cache[cache_key]
        
        # Step 3: Use LLM (slower but smart)
        print(f"🤖 Using LLM...")
        
        # Simplified prompt for speed
        prompt = f"<s>[INST] You are Swiggy support. Be brief and helpful.\n\nUser: {user_message}\n[/INST]"
        
        # Generate with optimized settings
        response = self.llm(
            prompt,
            max_tokens=150,      # Reduced from 256 (faster)
            temperature=0.7,
            top_p=0.95,
            top_k=40,
            repeat_penalty=1.1,
            stop=["User:", "\n\n"],
            echo=False
        )
        
        result = response['choices'][0]['text'].strip()
        
        # Cache the response
        self.response_cache[cache_key] = result
        
        elapsed = time.time() - start_time
        print(f"✅ LLM response ({elapsed:.2f}s)")
        
        return result