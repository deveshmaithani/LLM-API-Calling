from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()  
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def review_java_code(code: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a senior Java engineer with 10 years experience.
                Review the given code for:
                1. Bugs and logical errors
                2. Performance issues
                3. Bad practices
                4. Security vulnerabilities
                Be specific, be strict."""
            },
            {
                "role": "user",
                "content": f"Review this Java code:\n\n{code}"
            }
        ]
    )
    return response.choices[0].message.content

# Test it
sample_code = """
public List getUsers() {
    return jdbcTemplate.query("SELECT * FROM users");
}
"""

print(review_java_code(sample_code))