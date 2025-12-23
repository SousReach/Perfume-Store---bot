"""
Perfume Store AI Bot with Training Data - Python 3.14 Compatible
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import json
import random
import uvicorn
from datetime import datetime

app = FastAPI()

# Enable CORS for Android app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== MODELS ==========
class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    suggestions: List[str] = []
    confidence: float
    timestamp: str

# ========== LOAD TRAINING DATA ==========
def load_training_data():
    """Load perfumes from training_data.json"""
    try:
        with open('training_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            perfumes = data.get("perfumes", [])
            faqs = data.get("faqs", [])
            intents = data.get("intents", [])
            
            # Add IDs to perfumes if not present
            for i, perfume in enumerate(perfumes):
                if 'id' not in perfume:
                    perfume['id'] = i + 1
            
            print(f"✅ Loaded: {len(perfumes)} perfumes, {len(faqs)} FAQs, {len(intents)} intents")
            return perfumes, faqs, intents
            
    except FileNotFoundError:
        print("⚠️ training_data.json not found. Using default perfumes.")
        # Return default perfumes if file doesn't exist
        return [
            {"id": 1, "name": "Floral Dream", "price": 45.99, "category": "floral"},
            {"id": 2, "name": "Woody Essence", "price": 59.99, "category": "woody"},
            {"id": 3, "name": "Citrus Splash", "price": 39.99, "category": "citrus"},
        ], [], []
    except json.JSONDecodeError:
        print("❌ Error: training_data.json has invalid JSON format")
        return [], [], []

# Load data on startup
PERFUMES, FAQS, INTENTS = load_training_data()

# ========== AI LOGIC ==========
class PerfumeAI:
    def __init__(self):
        self.perfumes = PERFUMES
        self.faqs = FAQS
        self.intents = INTENTS
        
    def find_intent(self, message: str) -> str:
        """Detect user intent"""
        msg_lower = message.lower()
        
        # Check intents from training data
        for intent in self.intents:
            for pattern in intent.get('patterns', []):
                if pattern.lower() in msg_lower:
                    return intent.get('name', 'unknown')
        
        # Fallback intent detection
        if any(word in msg_lower for word in ["hi", "hello", "hey"]):
            return "greeting"
        elif any(word in msg_lower for word in ["recommend", "suggest"]):
            return "recommendation"
        elif any(word in msg_lower for word in ["price", "how much", "cost"]):
            return "price_inquiry"
        elif any(word in msg_lower for word in ["floral", "woody", "citrus", "fresh", "oriental"]):
            return "category_query"
        
        return "unknown"
    
    def answer_faq(self, question: str) -> Optional[str]:
        """Answer FAQ questions"""
        question_lower = question.lower()
        
        for faq in self.faqs:
            faq_question = faq.get('question', '').lower()
            # Simple keyword matching
            if any(word in question_lower for word in faq_question.split()[:3]):
                return faq.get('answer')
        
        return None
    
    def find_perfume(self, query: str) -> Optional[Dict]:
        """Find perfume by name, category, or notes"""
        query_lower = query.lower()
        
        # Check by name
        for perfume in self.perfumes:
            if perfume.get('name', '').lower() in query_lower:
                return perfume
        
        # Check by category
        for perfume in self.perfumes:
            if perfume.get('category', '').lower() in query_lower:
                return perfume
        
        # Check by notes
        for perfume in self.perfumes:
            for note in perfume.get('notes', []):
                if note.lower() in query_lower:
                    return perfume
        
        return None
    
    def generate_response(self, message: str) -> Dict:
        """Generate AI response"""
        # Step 1: Try to answer FAQ
        faq_answer = self.answer_faq(message)
        if faq_answer:
            return {
                "response": faq_answer,
                "type": "faq",
                "confidence": 0.9
            }
        
        # Step 2: Try to find perfume
        perfume = self.find_perfume(message)
        if perfume:
            response = f"**{perfume['name']}**\n\n"
            response += f"💰 Price: ${perfume['price']}\n"
            
            if 'category' in perfume:
                response += f"🌸 Category: {perfume['category'].title()}\n"
            
            if 'notes' in perfume and perfume['notes']:
                response += f"🎀 Notes: {', '.join(perfume['notes'][:3])}\n"
            
            if 'description' in perfume:
                response += f"\n{perfume['description']}"
            
            return {
                "response": response,
                "type": "perfume_info",
                "confidence": 0.8,
                "perfume": perfume
            }
        
        # Step 3: Handle intents
        intent = self.find_intent(message)
        
        if intent == "greeting":
            responses = [
                "👋 Hello! Welcome to our perfume store! How can I help you today?",
                "🌟 Welcome to our fragrance boutique! What scent are you looking for?",
                "🌸 Hello there! Ready to find your perfect fragrance?"
            ]
            return {
                "response": random.choice(responses),
                "type": "greeting",
                "confidence": 0.9
            }
        
        elif intent == "recommendation":
            if self.perfumes:
                # Get top 3 perfumes (by price or random)
                recommended = random.sample(self.perfumes, min(3, len(self.perfumes)))
                response = "✨ **Top Recommendations:**\n\n"
                for perfume in recommended:
                    response += f"⭐ **{perfume['name']}** - ${perfume['price']}\n"
                    if 'description' in perfume:
                        response += f"   {perfume['description']}\n\n"
                
                return {
                    "response": response,
                    "type": "recommendation",
                    "confidence": 0.8,
                    "perfumes": recommended
                }
        
        elif intent == "price_inquiry":
            if self.perfumes:
                response = "💰 **Our Perfume Prices:**\n\n"
                for perfume in self.perfumes[:5]:  # Show first 5
                    response += f"• {perfume['name']}: ${perfume['price']}\n"
                
                return {
                    "response": response,
                    "type": "price_info",
                    "confidence": 0.7
                }
        
        elif intent == "category_query":
            # Find which category was mentioned
            categories = ["floral", "woody", "citrus", "fresh", "oriental"]
            mentioned_category = next((cat for cat in categories if cat in message.lower()), None)
            
            if mentioned_category:
                filtered = [p for p in self.perfumes if p.get('category') == mentioned_category]
                if filtered:
                    response = f"🌸 **{mentioned_category.title()} Perfumes:**\n\n"
                    for perfume in filtered:
                        response += f"• **{perfume['name']}** - ${perfume['price']}\n"
                    return {
                        "response": response,
                        "type": "category_info",
                        "confidence": 0.8
                    }
        
        # Step 4: Fallback response
        fallback_responses = [
            "I'm not sure I understood. Try asking about specific perfumes or categories.",
            "Could you be more specific? For example, ask about 'Floral Dream' or 'woody perfumes'.",
            "I'm here to help you find perfumes! Try asking for recommendations or checking prices."
        ]
        
        return {
            "response": random.choice(fallback_responses),
            "type": "fallback",
            "confidence": 0.3
        }

# Initialize AI
ai = PerfumeAI()

# ========== HELPER FUNCTIONS ==========
def get_suggestions(response_type: str, message: str) -> List[str]:
    """Generate context-aware suggestions"""
    msg_lower = message.lower()
    
    suggestions = []
    
    if response_type == "perfume_info":
        suggestions = ["Similar perfumes", "Price range", "Show all", "Recommendations"]
    
    elif response_type == "faq":
        suggestions = ["More FAQs", "Perfume catalog", "Contact support"]
    
    elif any(word in msg_lower for word in ["recommend", "suggest"]):
        # Get unique categories from perfumes
        categories = list(set(p.get('category', '').title() for p in PERFUMES if p.get('category')))
        suggestions = categories[:3] + ["Show all", "Prices"]
    
    elif any(word in msg_lower for word in ["price", "how much", "cost"]):
        suggestions = [p['name'] for p in PERFUMES[:3]] + ["All prices", "Budget options"]
    
    else:
        suggestions = ["Recommend perfume", "Show all", "FAQs", "Help"]
    
    return suggestions

# ========== API ENDPOINTS ==========
@app.get("/")
async def root():
    """API information"""
    return {
        "service": "Perfume Store AI Bot",
        "version": "2.0",
        "perfumes_count": len(PERFUMES),
        "faqs_count": len(FAQS),
        "endpoints": {
            "GET /": "This information",
            "POST /chat": "Chat with AI bot",
            "GET /perfumes": "Get all perfumes",
            "GET /perfumes/{id}": "Get specific perfume",
            "GET /categories": "Get all categories"
        }
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with the AI perfume assistant"""
    try:
        ai_result = ai.generate_response(request.message)
        suggestions = get_suggestions(ai_result['type'], request.message)
        
        return ChatResponse(
            response=ai_result['response'],
            suggestions=suggestions,
            confidence=ai_result['confidence'],
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/perfumes")
async def get_perfumes():
    """Get all perfumes"""
    return PERFUMES

@app.get("/perfumes/{perfume_id}")
async def get_perfume(perfume_id: int):
    """Get specific perfume by ID"""
    perfume = next((p for p in PERFUMES if p['id'] == perfume_id), None)
    if perfume:
        return perfume
    raise HTTPException(status_code=404, detail="Perfume not found")

@app.get("/categories")
async def get_categories():
    """Get all available perfume categories"""
    categories = list(set(p.get('category', '') for p in PERFUMES if p.get('category')))
    return {"categories": [c.title() for c in categories if c]}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "perfumes_loaded": len(PERFUMES) > 0,
        "timestamp": datetime.now().isoformat()
    }

# ========== RUN SERVER ==========
if __name__ == "__main__":
    print("Perfume AI Bot with Training Data")
    print(f"Data Loaded: {len(PERFUMES)} perfumes, {len(FAQS)} FAQs")
    print(f"Server: http://localhost:8000")
    print(f"Docs: http://localhost:8000/docs")
    print(f"Data: http://localhost:8000/perfumes")
    print("\nPress Ctrl+C to stop\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False
    )