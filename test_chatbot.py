import requests
import json
import time
from colorama import init, Fore, Back, Style
init()

class ChatbotTester:
    def __init__(self):
        self.api_url = "http://localhost:8000"
        self.session_id = f"test_session_{int(time.time())}"
        self.test_results = []
        
    def print_header(self, text):
        print(f"\n{Back.BLUE}{Fore.WHITE} {text} {Style.RESET_ALL}")
    
    def print_success(self, text):
        print(f"{Fore.GREEN}✅ {text}{Style.RESET_ALL}")
    
    def print_error(self, text):
        print(f"{Fore.RED}❌ {text}{Style.RESET_ALL}")
    
    def print_info(self, text):
        print(f"{Fore.YELLOW}ℹ️  {text}{Style.RESET_ALL}")
    
    def test_server_health(self):
        """Test if server is running"""
        self.print_header("Testing Server Health")
        try:
            response = requests.get(f"{self.api_url}/health")
            if response.status_code == 200:
                self.print_success("Server is healthy")
                return True
            else:
                self.print_error("Server health check failed")
                return False
        except:
            self.print_error("Cannot connect to server. Run: python app.py")
            return False
    
    def test_chat_endpoint(self, message, expected_keywords=[]):
        """Test chat endpoint with a message"""
        self.print_info(f"Testing: '{message}'")
        
        try:
            response = requests.post(
                f"{self.api_url}/chat",
                json={
                    "message": message,
                    "session_id": self.session_id
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                bot_response = data['response']
                
                # Print bot response
                print(f"{Fore.CYAN}Bot: {bot_response[:200]}{'...' if len(bot_response) > 200 else ''}{Style.RESET_ALL}")
                
                # Check for expected keywords
                if expected_keywords:
                    found = any(keyword.lower() in bot_response.lower() for keyword in expected_keywords)
                    if found:
                        self.print_success(f"Response contains expected keywords")
                        return True
                    else:
                        self.print_error(f"Expected keywords not found: {expected_keywords}")
                        return False
                else:
                    self.print_success("Response received")
                    return True
            else:
                self.print_error(f"Chat endpoint failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all test cases"""
        print(f"\n{Back.MAGENTA}{Fore.WHITE} 🧪 SWIGGY CHATBOT TEST SUITE {Style.RESET_ALL}")
        print(f"{Fore.CYAN}Session ID: {self.session_id}{Style.RESET_ALL}")
        
        # Check server health first
        if not self.test_server_health():
            print(f"\n{Fore.RED}Please start the server first!{Style.RESET_ALL}")
            return
        
        # Test cases
        test_cases = [
            {
                "category": "Order Tracking",
                "tests": [
                    ("Track order ORD100000", ["delivered", "domino"]),
                    ("Where is my order ORD100001", ["preparing", "biryani"]),
                    ("Check status of ORD100002", ["out for delivery", "burger"]),
                    ("ORD100003 status", ["cancelled", "refund"]),
                    ("Track order ORD999999", ["not found", "couldn't find"]),
                ]
            },
            {
                "category": "Restaurant Search",
                "tests": [
                    ("Show pizza restaurants", ["domino", "pizza"]),
                    ("Find biryani places", ["biryani"]),
                    ("burger restaurants near me", ["burger"]),
                    ("Show popular restaurants", ["popular", "rating"]),
                    ("Quick delivery restaurants", ["quick", "fast", "20 min", "30 min"]),
                ]
            },
            {
                "category": "Menu Queries",
                "tests": [
                    ("Show menu for Domino's", ["margherita", "pizza", "₹"]),
                    ("What's on Burger King menu", ["whopper", "burger"]),
                    ("Menu", ["restaurant", "which"]),
                ]
            },
            {
                "category": "General Queries",
                "tests": [
                    ("Hi", ["hello", "welcome", "help"]),
                    ("I need help", ["help", "assist"]),
                    ("What can you do", ["order", "restaurant", "help"]),
                ]
            },
            {
                "category": "Hindi Support",
                "tests": [
                    ("मेरा ऑर्डर कहाँ है", ["order", "id"]),
                    ("पिज़्ज़ा दिखाओ", ["pizza", "domino"]),
                ]
            }
        ]
        
        # Run tests by category
        total_tests = 0
        passed_tests = 0
        
        for category in test_cases:
            self.print_header(f"Testing: {category['category']}")
            
            for test_message, keywords in category['tests']:
                total_tests += 1
                if self.test_chat_endpoint(test_message, keywords):
                    passed_tests += 1
                time.sleep(1)  # Avoid overwhelming the server
                print("-" * 50)
        
        # Print summary
        print(f"\n{Back.GREEN if passed_tests == total_tests else Back.YELLOW}{Fore.WHITE} TEST SUMMARY {Style.RESET_ALL}")
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {Fore.GREEN}{passed_tests}{Style.RESET_ALL}")
        print(f"Failed: {Fore.RED}{total_tests - passed_tests}{Style.RESET_ALL}")
        print(f"Success Rate: {Fore.CYAN}{(passed_tests/total_tests)*100:.1f}%{Style.RESET_ALL}")
        
        # Test API endpoints
        self.test_api_endpoints()
    
    def test_api_endpoints(self):
        """Test additional API endpoints"""
        self.print_header("Testing API Endpoints")
        
        endpoints = [
            ("/api/restaurants?query=pizza", "Restaurant Search API"),
            ("/api/order/ORD100000", "Order Tracking API"),
            ("/api/menu/REST001", "Menu API"),
            (f"/api/history/{self.session_id}", "Chat History API"),
            ("/api/stats", "Statistics API"),
        ]
        
        for endpoint, name in endpoints:
            try:
                response = requests.get(f"{self.api_url}{endpoint}")
                if response.status_code == 200:
                    self.print_success(f"{name}: Working")
                else:
                    self.print_error(f"{name}: Failed ({response.status_code})")
            except:
                self.print_error(f"{name}: Connection failed")

if __name__ == "__main__":
    tester = ChatbotTester()
    tester.run_all_tests()