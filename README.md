# Multi-AI Query Tool

This simple command-line tool sends a question to multiple AI services in parallel and prints their replies. Supported services include OpenAI, Anthropic (Claude), and Google's Gemini.

## Setup

1. Create a `.env` file in this directory with the following variables:
   ```
   OPENAI_API_KEY="your_openai_api_key"
   ANTHROPIC_API_KEY="your_anthropic_api_key"
   GOOGLE_API_KEY="your_google_api_key"
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script and enter a question at the prompt. Type `exit` to quit:

```bash
python multi_ai_query.py
```
