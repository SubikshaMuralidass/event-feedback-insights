from google.genai import Client
from app.config import GEMINI_API_KEY
import logging

client = Client(api_key=GEMINI_API_KEY)

def summarize_feedback(comments: list[str], model: str = "models/gemini-2.5-flash") -> str:  # Updated to a supported model
    if not comments:
        return "No feedback provided."
    
    prompt = f"""
        Summarize the following event feedback into a concise professional summary:

Feedback:
{chr(10).join(comments)}
"""
    
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )
        if response and response.text:
            return response.text.strip()
        else:
            return "No summary generated."
    except Exception as e:
        logging.error(f"Gemini API error: {e}")
        # Optional fallback to another model if this one fails
        if "NOT_FOUND" in str(e) and model != "models/gemini-2.5-pro":
            logging.info("Trying fallback model...")
            return summarize_feedback(comments, model="models/gemini-2.5-pro")
        return f"Failed to summarize: {str(e)}"