# main.py

import asyncio

from dotenv import load_dotenv
from google import genai
from google.genai import types

from models import Message

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


async def get_reply(history: list[Message]) -> str:
    """Send the whole conversation to the model and return its reply."""
    response = await client.aio.models.generate_content(
        model=MODEL,
        contents=to_gemini(history),
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            # No tools are used, so turn off automatic function calling (silences the AFC warning)
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
        ),
    )
    return response.text


async def main() -> None:
    history: list[Message] = []

    while True:
        user_input = await asyncio.to_thread(input, "You: ")
        if user_input == "quit":
            break

        history.append(Message(role="user", content=user_input))
        reply = await get_reply(history)
        history.append(Message(role="assistant", content=reply))
        print(f"Bot: {reply}")

    print(f"{len(history)} messages in history")


if __name__ == "__main__":
    asyncio.run(main())