# llm-building-blocks

Core LLM application patterns in Python, built from scratch.

## Contents

| Folder | What it does |
|---|---|
| `terminal-chat/` | Command-line chat with Gemini, using async calls and validated message history |

## Setup

```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file at the repo root with a Gemini API key from Google AI Studio:

```
GEMINI_API_KEY=your-key-here
```

## Run

```bash
cd terminal-chat
python main.py
```

Type `quit` to exit.

## Stack

Python 3.14, Pydantic, Google Gen AI SDK