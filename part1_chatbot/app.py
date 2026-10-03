import os
import uuid
import psycopg2
from dotenv import load_dotenv
from groq import Groq

from catalog import format_catalog_for_prompt

load_dotenv()

# Client setup
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("Warning: GROQ_API_KEY is not set. LLM calls will fail.")

client = Groq(api_key=GROQ_API_KEY)

# Policy & Help Desk Information
CUSTOMER_SUPPORT_CONTACT = "+1-800-456-7890 (Toll-Free, 9:00 AM - 7:00 PM IST)"
ESCALATION_KEYWORDS = {
    "return", "refund", "replace", "replacement", 
    "discount", "offer", "coupon", "promo", "voucher",
    "track order", "delivery delay", "human", "agent"
}

def get_db_connection():
    """Establish and return a database connection."""
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "chatbot_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )

def log_conversation(session_id: str, user_query: str, bot_reply: str, was_redirected: bool):
    """Safely log interaction to PostgreSQL without breaking chat flow on db failure."""
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO conversation_logs (session_id, user_query, bot_reply, was_redirected)
                VALUES (%s, %s, %s, %s);
                """,
                (session_id, user_query, bot_reply, was_redirected)
            )
            conn.commit()
    except Exception as err:
        # Avoid crashing user session if logging hits an intermittent network glitch
        print(f"[Log Error] Failed to persist message: {err}")
    finally:
        if conn:
            conn.close()

def is_support_inquiry(text: str) -> bool:
    """Check if query requires customer support or deals with commercial policies."""
    tokens = set(text.lower().split())
    # Substring checks for compound words like 'discounts' or 'refunds'
    return any(keyword in text.lower() for keyword in ESCALATION_KEYWORDS)

def run_chat_pipeline(session_id: str, user_message: str) -> str:
    cleaned_input = user_message.strip()
    if not cleaned_input:
        return "Please enter a question or product inquiry."

    # 1. Deterministic guardrail check (Escalation route)
    if is_support_inquiry(cleaned_input):
        reply = (
            "For assistance with returns, refunds, order tracking, or current promotional offers, "
            f"please connect with our support team at {CUSTOMER_SUPPORT_CONTACT}. "
            "A representative will assist you directly."
        )
        log_conversation(session_id, cleaned_input, reply, was_redirected=True)
        return reply

    # 2. General advisory and product recommendation route
    system_instructions = (
        "You are an approachable, knowledgeable personal care consultant for an online boutique.\n"
        "Guidelines:\n"
        "- Answer the customer's question directly and concisely (under 4 sentences).\n"
        "- Recommend relevant products from the provided catalog when appropriate.\n"
        "- If a user asks about benefits, explain the active ingredients naturally without medical jargon.\n"
        "- Do not fabricate prices or inventory outside the catalog.\n\n"
        f"Available Inventory:\n{format_catalog_for_prompt()}"
    )

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": cleaned_input}
            ],
            temperature=0.4,
            max_tokens=220
        )
        reply = response.choices[0].message.content.strip()
        log_conversation(session_id, cleaned_input, reply, was_redirected=False)
        return reply

    except Exception as api_err:
        fallback_msg = (
            "I'm temporarily having trouble fetching that information. "
            "Please try again in a moment."
        )
        print(f"[LLM API Error] {api_err}")
        return fallback_msg

if __name__ == "__main__":
    current_session = str(uuid.uuid4())[:8]
    print(f"=== Personal Care Assistant (Session: {current_session}) ===")
    print("Ask about grooming tips, ingredients, or products. Type 'quit' to end.\n")

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower().strip() in {"quit", "exit", "q"}:
                print("Session closed.")
                break
            
            answer = run_chat_pipeline(current_session, user_input)
            print(f"\nAssistant: {answer}\n")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break