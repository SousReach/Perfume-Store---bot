"""
Enhanced Perfume AI Bot with Training Capabilities
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
import uvicorn

# Import our trainer
from trainer import PerfumeAITrainer

# ========== MODELS ==========
class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    suggestions: List[str] = []
    confidence: float
    timestamp: str

# ========== FASTAPI APP ==========
app = FastAPI(
    title="Perfume Store AI Bot",
    description="AI Assistant with Training",
    version="2.0"
)

# Enable CORS for Android app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI Trainer
trainer = PerfumeAITrainer("training_data.json")

# ========== HELPER FUNCTIONS ==========
def get_suggestions(response_type: str, message: str) -> List[str]:
    """Generate context-aware suggestions"""
    message_lower = message.lower()
    
    if response_type == "perfume_info":
        return ["Similar perfumes", "Price range", "Show all", "Recommendations"]
    
    elif response_type == "faq":
        return ["More FAQs", "Perfume catalog", "Contact support", "Help"]
    
    elif any(word in message_lower for word in ["recommend", "suggest"]):
        categories = list(set(p['category'] for p in trainer.perfumes))
        return categories[:3] + ["Show all", "Prices"]
    
    elif any(word in message_lower for word in ["price", "how much", "cost"]):
        return ["Floral Dream price", "Woody Essence price", "All prices", "Budget options"]
    
    else:
        return ["Recommend perfume", "Show all", "FAQs", "Help"]

# ========== API ENDPOINTS ==========
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Perfume Store AI Bot",
        "version": "2.0",
        "training_data": {
            "perfumes": len(trainer.perfumes),
            "faqs": len(trainer.faqs),
            "intents": len(trainer.intents)
        }
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint with trained AI"""
    try:
        # Generate AI response
        ai_result = trainer.generate_response(request.message)
        
        # Get suggestions
        suggestions = get_suggestions(ai_result['type'], request.message)
        
        return ChatResponse(
            response=ai_result['response'],
            suggestions=suggestions,
            confidence=ai_result['confidence'],
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")

@app.get("/perfumes")
async def get_perfumes():
    """Get all perfumes"""
    return trainer.perfumes

# ========== RUN SERVER ==========
if __name__ == "__main__":
    print("🤖 Perfume AI Bot with Training")
    print(f"📊 Training Data: {len(trainer.perfumes)} perfumes, {len(trainer.faqs)} FAQs, {len(trainer.intents)} intents")
    print("\n🚀 Server: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)