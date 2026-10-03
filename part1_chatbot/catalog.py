products = [
    {
        "id": "PROD01",
        "name": "HydraBoost Hyaluronic Acid Serum",
        "category": "Serum",
        "skin_type": "Dry and dehydrated skin",
        "price": 599,
        "benefits": "Provides deep hydration, plumps skin, and reduces tightness.",
        "usage": "Apply 2-3 drops on damp skin before applying moisturizer."
    },
    {
        "id": "PROD02",
        "name": "Tea Tree Clarifying Face Wash",
        "category": "Cleanser",
        "skin_type": "Oily and acne-prone skin",
        "price": 349,
        "benefits": "Controls extra oil, unclogs pores, and prevents pimples.",
        "usage": "Take a coin-sized amount, rub gently on wet face, and wash off with water."
    },
    {
        "id": "PROD03",
        "name": "Niacinamide 10% Daily Face Gel",
        "category": "Moisturizer",
        "skin_type": "Normal to combination skin",
        "price": 499,
        "benefits": "Fades dark acne marks, minimizes open pores, and balances oil production.",
        "usage": "Take a pea-sized amount and gently massage all over face morning and evening."
    },
    {
        "id": "PROD04",
        "name": "Matte Finish Sunscreen Gel SPF 50",
        "category": "Sun Protection",
        "skin_type": "All skin types",
        "price": 450,
        "benefits": "Protects from UVA/UVB rays, leaves zero white cast, and gives a non-sticky feel.",
        "usage": "Apply two finger lengths of sunscreen 15 minutes before stepping out in the sun."
    }
]

def format_catalog_for_prompt():
    catalog_text = ""
    for p in products:
        catalog_text += f"- {p['name']} ({p['category']}) - Price: Rs. {p['price']}\n"
        catalog_text += f"  Best for: {p['skin_type']}\n"
        catalog_text += f"  Benefits: {p['benefits']}\n"
        catalog_text += f"  How to use: {p['usage']}\n\n"
    return catalog_text.strip()