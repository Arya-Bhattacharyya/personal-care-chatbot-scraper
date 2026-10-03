"""
Dummy catalog for Personal Care POC.
In a production setup, this would be queried from an inventory database or vector store.
"""

PRODUCTS = [
    {
        "id": "SKIN-001",
        "name": "DermaGlow 10% Vitamin C Serum",
        "category": "Face Care",
        "skin_type": "Dull, uneven skin tone",
        "price": 649,
        "benefits": "Lightens hyperpigmentation, stimulates collagen, provides antioxidant defense.",
        "usage": "Smooth 3-4 drops onto a clean face each morning before applying moisturizer and SPF."
    },
    {
        "id": "SKIN-002",
        "name": "Ceramide Barrier Defense Cream",
        "category": "Moisturizer",
        "skin_type": "Dry, sensitive, or compromised barrier",
        "price": 520,
        "benefits": "Restores lipid moisture levels, prevents transepidermal water loss, calms redness.",
        "usage": "Warm a dime-sized amount between fingertips and pat gently across face and neck."
    },
    {
        "id": "SKIN-003",
        "name": "BHA 2% Salicylic Cleansing Gel",
        "category": "Cleanser",
        "skin_type": "Oily, acne-prone",
        "price": 380,
        "benefits": "Penetrates sebum inside pores, clears blackheads, reduces active breakouts.",
        "usage": "Massage onto damp skin for 60 seconds once or twice daily, then rinse thoroughly."
    },
    {
        "id": "GROOM-001",
        "name": "Cedarwood & Jojoba Conditioning Beard Oil",
        "category": "Men's Grooming",
        "skin_type": "All facial hair types / dry underlying skin",
        "price": 450,
        "benefits": "Softens coarse beard strands, stops flaking/beard dandruff, non-greasy finish.",
        "usage": "Distribute 4-6 drops evenly into hands and work through beard down to the roots."
    }
]

def format_catalog_for_prompt() -> str:
    lines = []
    for item in PRODUCTS:
        lines.append(
            f"- {item['name']} (₹{item['price']}) [{item['category']}]: "
            f"Target: {item['skin_type']}. "
            f"Key Benefits: {item['benefits']} "
            f"Directions: {item['usage']}"
        )
    return "\n".join(lines)