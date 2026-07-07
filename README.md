# crewai-demo

# openai-api
This is a very common and practical development task. Because you haven't specified your language or existing tool framework, I will provide a conceptual, multi-step guide using **Python** as the primary example, as Python is typically used for rapid CLI scripting due to its excellent support for APIs and argument parsing.

The key concept here is *Separation of Concerns*: Your main CLI logic should not contain API keys or complex API calling code. You must wrap the entire OpenAI interaction into a dedicated module (a service layer).

---

## 🚀 The Step-by-Step Setup Guide

### Phase 0: Prerequisites and Security (Crucial)

#### 1. Get the SDK
Install the official OpenAI Python library:
```bash
pip install openai pydantic # You might also need 'pydantic' for structured output
```

#### 2. Securely Handle the API Key
**NEVER hardcode your API key.** Use environment variables.

*   **Linux/macOS:**
    ```bash
    export OPENAI_API_KEY="sk-*********************"
    ```
*   **Windows (Command Prompt):**
    ```bash
    set OPENAI_API_KEY=sk-*********************
    ```

### Phase 1: Creating the Service Layer (The Wrapper)

This is the most critical step. You will create a module, let's call it `openai_handler.py`, whose sole job is to manage connection and interaction with OpenAI. This keeps your main CLI code clean.

**`my_cli/openai_handler.py`:**
```python
import os
from openai import OpenAI
from typing import Optional

# Initialize the client. It automatically looks for OPENAI_API_KEY
# in the environment variables.
try:
    client = OpenAI()
except Exception as e:
    print("Error initializing OpenAI client.")
    raise e # Re-raise or handle appropriately

def get_openai_response(prompt: str, model: str = "gpt-3.5-turbo") -> Optional[str]:
    """
    Sends a prompt to the OpenAI API and returns the text response.
    Handles connection and API errors.
    """
    print(f"\n--- Calling OpenAI ({model}) ---")
    try:
        # 1. Make the call
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful CLI assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7 # Adjust creativity here
        )
        # 2. Extract the text response
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"\n🚨 ERROR during API call: {e}")
        # Return None or raise a custom exception to signal failure gracefully
        return None
```

### Phase 2: Building the CLI Interface (The Main Tool)

Now, your main entry point for the CLI tool (`main.py`) only needs to worry about accepting arguments and calling the wrapper function.

We use a library like `argparse` or `click` to handle command-line inputs cleanly.

**`my_cli/main.py`:**
```python
import argparse
from openai_handler import get_openai_response # Import your service layer

def run_cli(prompt: str, model: str):
    """
    The main function that orchestrates the CLI workflow.
    It does NOT contain API logic itself.
    """
    print("=======================================")
    print(f"🤖 Tool initialized. Sending prompt to AI.")
    print(f"   Prompt: '{prompt}'")

    # Call the isolated wrapper function
    ai_response = get_openai_response(prompt, model)

    # Handle the response state
    if ai_response:
        print("\n=======================================")
        print("✅ AI Response:")
        print("---------------------------------------")
        # Print the result in a clean format
        print(ai_response)
        print("=======================================\n")
    else:
        print("\n❌ Failed to get response. Please check your API key and network connection.")


def main():
    parser = argparse.ArgumentParser(description="A CLI tool powered by OpenAI.")
    parser.add_argument("prompt", type=str, help="The question or task you want the AI to perform.")
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo",
                        help="Specify the OpenAI model (e.g., gpt-4).")

    args = parser.parse_args()
    run_cli(args.prompt, args.model)

if __name__ == "__main__":
    main()
```

### Phase 3: Testing and Execution

1.  **Run the tool:**
    ```bash
    python my_cli/main.py "Explain the concept of quantum entanglement in simple terms." --model gpt-3.5-turbo
    ```

2.  **What happens internally?**
    *   `main()` parses arguments (`prompt`, `--model`).
    *   `main()` calls `get_openai_response()`.
    *   `get_openai_response()` uses the environment variable key, constructs the API request, handles potential exceptions (like rate limits), and returns the clean text.
    *   `main()` receives the result and formats it for the user.

---

## ✨ Summary of Best Practices

| Principle | Implementation Step | Why It Matters |
| :--- | :--- | :--- |
| **Isolation** | Create a dedicated `openai_handler.py` file (The Wrapper). | Keeps your core business logic separate from network/API concerns. Makes debugging easier. |
| **Security** | Always load the API key via Environment Variables (`os.environ`). | Prevents accidentally committing sensitive keys to source control (Git). |
| **Robustness** | Use `try...except` blocks around all API calls. | APIs fail for many reasons (rate limits, bad input, network issues). Your CLI tool must not crash; it must report the error gracefully. |
| **User Experience** | Use a dedicated CLI argument parser (`argparse`, `click`). | Allows users to interact with your tool professionally (e.g., `my_cli --help`). |

