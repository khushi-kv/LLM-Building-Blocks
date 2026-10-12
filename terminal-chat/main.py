# main.py

import asyncio

from dotenv import load_dotenv
from google import genai
from google.genai import types

from models import Message, QueryAnalysis

from collections.abc import AsyncIterable

load_dotenv()              # reads GEMINI_API_KEY from .env
client = genai.Client()    # picks the key up automatically
MODEL = "gemini-3.5-flash-lite"
SYSTEM_PROMPT = "You are a helpful assistant."


def to_gemini(history: list[Message]) -> list[dict]:
    """Convert our messages into the format Gemini expects."""
    return [
        {
            "role": "model" if m.role == "assistant" else "user",
            "parts": [{"text": m.content}],
        }
        for m in history
    ]


async def analyze_query(text: str) -> QueryAnalysis:
    """Force Gemini to output strictly validated JSON matching our Pydantic schema."""
    response = await client.aio.models.generate_content(
        model=MODEL,
        contents=f"Analyze this user query: {text}",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=QueryAnalysis,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
        ),
    )
    return QueryAnalysis.model_validate_json(response.text)


async def get_reply_stream(history: list[Message]) -> AsyncIterable[str]:
    """Stream response chunks from the model as they arrive."""
    response_stream = await client.aio.models.generate_content_stream(
        model=MODEL,
        contents=to_gemini(history),
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
        ),
    )
    async for chunk in response_stream:
        if chunk.text:
            yield chunk.text


async def main() -> None:
    history: list[Message] = []

    while True:
        user_input = await asyncio.to_thread(input, "You: ")
        if user_input == "quit":
            break

        # Record user input
        history.append(Message(role="user", content=user_input))

        # 1. Structured JSON Analysis (forces Gemini to output typed Pydantic data)
        try:
            analysis = await analyze_query(user_input)
            print(f"[Analysis] Intent: {analysis.intent} | Sentiment: {analysis.sentiment} | Topics: {', '.join(analysis.topics)} (confidence: {analysis.confidence_score:.2f})")
        except Exception as e:
            print(f"[Analysis Error] {e}")

        # 2. Live Token-Streamed Conversational Response
        print("Bot: ", end="", flush=True)
        chunks: list[str] = []
        async for chunk in get_reply_stream(history):
            print(chunk, end="", flush=True)
            chunks.append(chunk)
        print()  # newline when response finishes
        full_reply = "".join(chunks)
        history.append(Message(role="assistant", content=full_reply))



if __name__ == "__main__":
    asyncio.run(main())