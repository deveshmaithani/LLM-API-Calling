from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()  
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

conversation_history = []

def chat_review(user_message: str) -> str:
    """Multi-turn — remembers context across messages"""
    
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a senior Java engineer doing an interactive 
                code review session. Remember all code shared in this conversation.
                Answer follow-up questions about the same code."""
            },
            *conversation_history  # full history every time
        ]
    )

    reply = response.choices[0].message.content
    conversation_history.append({
        "role": "assistant",
        "content": reply
    })
    return reply


# Now you can do this:
print(chat_review("Review this: public List getUsers() { return jdbcTemplate.query('SELECT * FROM users'); }"))
print(chat_review("How do I fix the security issue you mentioned?"))
print(chat_review("Show me the fixed version with pagination"))