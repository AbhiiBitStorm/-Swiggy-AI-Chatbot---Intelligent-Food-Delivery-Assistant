import json
import os
from datetime import datetime, timedelta
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

class ChatbotAnalytics:
    def __init__(self):
        self.data_dir = "data"
        self.load_conversations()
        
    def load_conversations(self):
        """Load conversation history"""
        conv_file = os.path.join(self.data_dir, "conversations.json")
        if os.path.exists(conv_file):
            with open(conv_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.conversations = data.get('conversations', [])
        else:
            self.conversations = []
    
    def generate_report(self):
        """Generate analytics report"""
        if not self.conversations:
            print("No conversation data available yet!")
            return
        
        print("\n" + "="*60)
        print(" SWIGGY CHATBOT ANALYTICS REPORT")
        print("="*60)
        
        # Basic stats
        total_conversations = len(self.conversations)
        unique_sessions = len(set(c['session_id'] for c in self.conversations))
        
        print(f"\n📊 OVERVIEW:")
        print(f"  Total Conversations: {total_conversations}")
        print(f"  Unique Sessions: {unique_sessions}")
        print(f"  Avg Messages/Session: {total_conversations/unique_sessions:.1f}")
        
        # Query Analysis
        self.analyze_queries()
        
        # Response Time Analysis
        self.analyze_response_patterns()
        
        # Popular Intents
        self.analyze_intents()
        
        # Generate visualizations
        self.create_visualizations()
    
    def analyze_queries(self):
        """Analyze user queries"""
        user_messages = [c['user_message'] for c in self.conversations]
        
        # Most common words
        all_words = ' '.join(user_messages).lower().split()
        word_freq = Counter(all_words)
        
        # Remove common words
        stop_words = {'i', 'the', 'is', 'my', 'a', 'to', 'and', 'of', 'in', 'for'}
        for word in stop_words:
            word_freq.pop(word, None)
        
        print(f"\n🔍 TOP KEYWORDS:")
        for word, count in word_freq.most_common(10):
            print(f"  {word}: {count}")
    
    def analyze_response_patterns(self):
        """Analyze response patterns"""
        print(f"\n⏱️ USAGE PATTERNS:")
        
        # Group by hour
        hours = []
        for conv in self.conversations:
            try:
                timestamp = datetime.fromisoformat(conv['timestamp'])
                hours.append(timestamp.hour)
            except:
                pass
        
        if hours:
            hour_counts = Counter(hours)
            peak_hour = hour_counts.most_common(1)[0][0]
            print(f"  Peak Usage Hour: {peak_hour}:00 - {peak_hour+1}:00")
    
    def analyze_intents(self):
        """Analyze user intents"""
        intents = {
            'order_tracking': 0,
            'restaurant_search': 0,
            'menu_query': 0,
            'general': 0
        }
        
        for conv in self.conversations:
            msg = conv['user_message'].lower()
            if any(word in msg for word in ['track', 'order', 'ord', 'status', 'where']):
                intents['order_tracking'] += 1
            elif any(word in msg for word in ['restaurant', 'pizza', 'biryani', 'burger', 'food']):
                intents['restaurant_search'] += 1
            elif 'menu' in msg:
                intents['menu_query'] += 1
            else:
                intents['general'] += 1
        
        print(f"\n🎯 USER INTENTS:")
        total = sum(intents.values())
        for intent, count in intents.items():
            percentage = (count/total*100) if total > 0 else 0
            print(f"  {intent.replace('_', ' ').title()}: {count} ({percentage:.1f}%)")
    
    def create_visualizations(self):
        """Create visualization charts"""
        try:
            # Set style
            sns.set_style("whitegrid")
            plt.figure(figsize=(15, 10))
            
            # 1. Messages over time
            plt.subplot(2, 2, 1)
            timestamps = []
            for conv in self.conversations:
                try:
                    timestamps.append(datetime.fromisoformat(conv['timestamp']))
                except:
                    pass
            
            if timestamps:
                plt.hist([t.hour for t in timestamps], bins=24, color='#fc8019', alpha=0.7)
                plt.xlabel('Hour of Day')
                plt.ylabel('Number of Messages')
                plt.title('Message Distribution by Hour')
            
            # 2. Intent Distribution
            plt.subplot(2, 2, 2)
            intents = self.get_intent_distribution()
            if intents:
                plt.pie(intents.values(), labels=intents.keys(), autopct='%1.1f%%', 
                       colors=['#fc8019', '#ff5722', '#ffa726', '#ffb74d'])
                plt.title('Query Intent Distribution')
            
            # 3. Session Length Distribution
            plt.subplot(2, 2, 3)
            session_lengths = self.get_session_lengths()
            if session_lengths:
                plt.bar(range(len(session_lengths)), session_lengths, color='#fc8019')
                plt.xlabel('Session')
                plt.ylabel('Number of Messages')
                plt.title('Messages per Session')
            
            # 4. Response Word Count
            plt.subplot(2, 2, 4)
            word_counts = [len(c['bot_response'].split()) for c in self.conversations[:20]]
            if word_counts:
                plt.plot(word_counts, marker='o', color='#fc8019')
                plt.xlabel('Response Number')
                plt.ylabel('Word Count')
                plt.title('Bot Response Length')
            
            plt.tight_layout()
            
            # Save figure
            output_file = 'chatbot_analytics.png'
            plt.savefig(output_file)
            print(f"\n📈 Visualization saved as: {output_file}")
            
        except Exception as e:
            print(f"\n⚠️ Could not create visualizations: {str(e)}")
            print("Install matplotlib and seaborn: pip install matplotlib seaborn")
    
    def get_intent_distribution(self):
        """Get intent distribution for pie chart"""
        intents = {
            'Order Tracking': 0,
            'Restaurant Search': 0,
            'Menu Query': 0,
            'General': 0
        }
        
        for conv in self.conversations:
            msg = conv['user_message'].lower()
            if any(word in msg for word in ['track', 'order', 'ord']):
                intents['Order Tracking'] += 1
            elif any(word in msg for word in ['restaurant', 'pizza', 'biryani']):
                intents['Restaurant Search'] += 1
            elif 'menu' in msg:
                intents['Menu Query'] += 1
            else:
                intents['General'] += 1
        
        return intents
    
    def get_session_lengths(self):
        """Get message count per session"""
        session_counts = Counter(c['session_id'] for c in self.conversations)
        return list(session_counts.values())[:10]  # Top 10 sessions

if __name__ == "__main__":
    analytics = ChatbotAnalytics()
    analytics.generate_report()