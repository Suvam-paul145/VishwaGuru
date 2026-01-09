import os
import google.generativeai as genai
from typing import Optional
import warnings
from async_lru import alru_cache
from retry_utils import exponential_backoff_retry
import logging
import json

# Configure logging
logger = logging.getLogger(__name__)

# Suppress deprecation warnings from google.generativeai
warnings.filterwarnings("ignore", category=FutureWarning, module="google.generativeai")

# Configure Gemini
# Use provided key as fallback if env var is missing
api_key = os.environ.get("GEMINI_API_KEY", "AIzaSyB8_i3tbDE3GmX4CsQ8G3mD3pB2WrHi5C8")
if api_key:
    genai.configure(api_key=api_key)

def _get_fallback_action_plan(issue_description: str, category: str) -> dict:
    """Generate fallback action plan when AI is unavailable."""
    return {
        "whatsapp": f"Hello, I would like to report a {category} issue: {issue_description}",
        "email_subject": f"Complaint regarding {category}",
        "email_body": f"Respected Authority,\n\nI am writing to bring to your attention a {category} issue: {issue_description}.\n\nPlease take necessary action.\n\nSincerely,\nCitizen"
    }


@exponential_backoff_retry(max_retries=3, base_delay=1.0, max_delay=10.0)
async def _generate_action_plan_with_retry(issue_description: str, category: str) -> dict:
    """
    Internal function that generates action plan with retry logic.
    Raises exception on failure to allow retry decorator to work.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    You are a civic action assistant. A user has reported a civic issue.
    Category: {category}
    Description: {issue_description}

    Please generate:
    1. A concise WhatsApp message (max 200 chars) that can be sent to authorities.
    2. A formal but firm email subject.
    3. A formal email body (max 150 words) addressed to the relevant authority (e.g., Municipal Commissioner, Police, etc. based on category).

    Return the response in strictly valid JSON format with keys: "whatsapp", "email_subject", "email_body".
    Do not use markdown code blocks. Just the raw JSON string.
    """

    response = await model.generate_content_async(prompt)
    text_response = response.text.strip()

    # Cleanup if markdown code blocks are returned
    if text_response.startswith("```json"):
        text_response = text_response[7:-3]
    elif text_response.startswith("```"):
        text_response = text_response[3:-3]

    return json.loads(text_response)


async def generate_action_plan(issue_description: str, category: str, image_path: Optional[str] = None) -> dict:
    """
    Generates an action plan (WhatsApp message, Email draft) using Gemini.
    Includes retry logic with exponential backoff for transient failures.
    """
    if not api_key:
        logger.warning("No API key configured, using fallback action plan")
        return _get_fallback_action_plan(issue_description, category)

    try:
        return await _generate_action_plan_with_retry(issue_description, category)
    except Exception as e:
        logger.error(f"Gemini Error after all retries: {e}", exc_info=True)
        # Return fallback after all retries exhausted
        return _get_fallback_action_plan(issue_description, category)

@exponential_backoff_retry(max_retries=3, base_delay=1.0, max_delay=10.0)
async def _chat_with_civic_assistant_with_retry(query: str) -> str:
    """
    Internal function that handles chat with retry logic.
    Raises exception on failure to allow retry decorator to work.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    You are VishwaGuru, a helpful civic assistant for Indian citizens.
    User Query: {query}

    Answer the user's question about civic issues, government services, or local administration.
    If they ask about specific MLAs, tell them to use the "Find My MLA" feature.
    Keep answers concise and helpful.
    """

    response = await model.generate_content_async(prompt)
    return response.text.strip()


@alru_cache(maxsize=100)
async def chat_with_civic_assistant(query: str) -> str:
    """
    Chat with the civic assistant.
    Includes retry logic with exponential backoff for transient failures.
    """
    if not api_key:
        logger.warning("No API key configured, chat assistant offline")
        return "I am currently offline. Please try again later."

    try:
        return await _chat_with_civic_assistant_with_retry(query)
    except Exception as e:
        logger.error(f"Gemini Chat Error after all retries: {e}", exc_info=True)
        return "I encountered an error processing your request. Please try again later."
