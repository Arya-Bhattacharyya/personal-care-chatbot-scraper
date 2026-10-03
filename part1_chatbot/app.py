import os
import uuid
import psycopg2
from dotenv import load_dotenv
from groq import Groq
from catalog import format_catalog_for_prompt

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

support_phone = "+1-800-456-7890"

support_keywords = [
    "return", "refund", "replace", "exchange", 
    "discount", "offer", "coupon", "promo", 
    "order status", "delivery", "human", "agent"
]

def save_to_db(session_id, user_msg, bot_msg, redirected):
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "chatbot_db"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", ""),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432")
        )
        cur = conn.cursor()
        query = """
            INSERT INTO conversation_logs (session_id, user_query, bot_reply, was_redirected)
            VALUES (%s, %s, %s, %s);
        """
        cur.execute(query, (session_id, user_msg, bot_msg, redirected))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")

def check_support_request(text):
    lowered = text.lower()
    for word in support_keywords:
        if word in lowered:
            return True
    return False

def chat(session_id, user_input):
    msg = user_input.strip()
    if not msg:
        return "How can I help you today?"

    if check_support_request(msg):
        reply = f"For issues regarding returns, refunds, or current offers, please reach out directly to customer care at {support_phone}."
        save_to_db(session_id, msg, reply, True)
        return reply

    catalog_data = format_catalog_for_prompt()
    system_prompt = (
        "You are an assistant for a personal care brand. "
        "Recommend suitable products from the catalog and explain benefits simply in 2-3 sentences. "
        "Do not invent items that are not in the list.\n\n"
        f"Products:\n{catalog_data}"
    )

    try:
        res = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": msg}
            ],
            temperature=0.3,
            max_tokens=200
        )
        reply = res.choices[0].message.content.strip()
        save_to_db(session_id, msg, reply, False)
        return reply

    except Exception as e:
        print(f"Error calling model: {e}")
        return "Sorry, something went wrong while getting the response. Please try again."

if __name__ == "__main__":
    session_id = str(uuid.uuid4())[:8]
    print(f"Personal Care Assistant started (Session: {session_id})")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            user_text = input("User: ")
            if user_text.strip().lower() in ["exit", "quit", "q"]:
                print("Exiting...")
                break
            
            bot_text = chat(session_id, user_text)
            print(f"Bot: {bot_text}\n")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break