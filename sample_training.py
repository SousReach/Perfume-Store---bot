"""
Script to populate initial training data
"""

import json

# Sample training data
training_data = {
    "perfumes": [
        {
            "name": "Floral Dream",
            "category": "floral",
            "notes": ["Rose", "Jasmine", "Lily", "Peony"],
            "price": 45.99,
            "description": "A delicate floral bouquet perfect for daytime wear",
            "questions": [
                "What is Floral Dream?",
                "Tell me about Floral Dream",
                "Describe Floral Dream perfume",
                "What does Floral Dream smell like?"
            ],
            "answers": [
                "Floral Dream is a delicate floral bouquet with notes of Rose, Jasmine, Lily, and Peony. Perfect for daytime wear.",
                "It's a floral fragrance priced at $45.99, featuring Rose, Jasmine, Lily, and Peony notes.",
                "This perfume is a floral scent with Rose, Jasmine, Lily, and Peony notes. Great for spring and daytime events."
            ]
        },
        {
            "name": "Woody Essence",
            "category": "woody",
            "notes": ["Sandalwood", "Cedar", "Patchouli", "Vetiver"],
            "price": 59.99,
            "description": "Rich woody fragrance with warm undertones",
            "questions": [
                "What is Woody Essence?",
                "Tell me about woody perfumes",
                "Describe Woody Essence",
                "What are woody perfumes?"
            ],
            "answers": [
                "Woody Essence is a rich woody fragrance with Sandalwood, Cedar, Patchouli, and Vetiver notes. Priced at $59.99.",
                "It's a woody perfume with warm undertones, featuring Sandalwood, Cedar, Patchouli, and Vetiver.",
                "This is a unisex woody fragrance perfect for evening wear, priced at $59.99."
            ]
        }
    ],
    "faqs": [
        {
            "question": "How long does perfume last?",
            "answer": "Perfume longevity depends on concentration: Eau de Toilette lasts 3-4 hours, Eau de Parfum lasts 4-6 hours, and Parfum lasts 8+ hours."
        },
        {
            "question": "What's the difference between EDP and EDT?",
            "answer": "EDP (Eau de Parfum) has 15-20% fragrance oil and lasts longer. EDT (Eau de Toilette) has 5-15% oil and is lighter."
        },
        {
            "question": "How should I store perfume?",
            "answer": "Store perfume in a cool, dark place away from direct sunlight and temperature changes to preserve its scent."
        }
    ],
    "intents": [
        {
            "name": "greeting",
            "patterns": ["hello", "hi", "hey", "good morning", "good afternoon", "greetings"],
            "responses": [
                "Hello! Welcome to our perfume store! How can I help you today?",
                "Hi there! Looking for a new fragrance today?",
                "Welcome! I'm here to help you find the perfect perfume."
            ]
        },
        {
            "name": "recommendation",
            "patterns": [
                "recommend a perfume",
                "suggest a fragrance",
                "what should I buy",
                "help me choose",
                "what perfume is best",
                "can you recommend"
            ],
            "responses": [
                "I'd be happy to recommend a perfume! What type of scents do you prefer?",
                "Let me suggest some fragrances for you. Do you like floral, woody, or citrus scents?",
                "I can help you choose! Tell me about your scent preferences."
            ]
        },
        {
            "name": "price_inquiry",
            "patterns": [
                "how much is",
                "price of",
                "cost",
                "what's the price",
                "how expensive is",
                "price for"
            ],
            "responses": [
                "I can check the price for you. Which perfume are you interested in?",
                "Let me look up the price. Which fragrance would you like to know about?",
                "I'll check the cost for you. What's the name of the perfume?"
            ]
        },
        {
            "name": "category_query",
            "patterns": [
                "floral perfumes",
                "woody fragrances",
                "citrus scents",
                "show me floral",
                "what woody perfumes",
                "oriental perfumes"
            ],
            "responses": [
                "Let me show you those perfumes. Here's what we have in that category...",
                "I'll find those fragrances for you. Let me check our collection.",
                "Here are the perfumes in that category that we offer."
            ]
        }
    ]
}

# Save to file
with open("training_data.json", "w", encoding="utf-8") as f:
    json.dump(training_data, f, indent=2, ensure_ascii=False)

print("✅ Sample training data created: training_data.json")
print(f"• {len(training_data['perfumes'])} perfumes")
print(f"• {len(training_data['faqs'])} FAQs")
print(f"• {len(training_data['intents'])} intents")