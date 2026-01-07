# Copilot / AI Agent Instructions

Purpose
- Help an AI coding assistant be productive in this Streamlit chatbot repo (Darwin).

Big picture
- This is a small Streamlit-based chatbot app. The primary user-facing entry is [streamlit_app.py](streamlit_app.py).
- Experimental notebooks and scripts live in the repo root (e.g., `chatbot project.ipynb`, `my first chatbot.py`, `second_chatbot.py`, `prototype.ipynb`). Treat notebooks as experiments, not canonical code.

Runtime & dev workflow
- Install deps: `pip install -r requirements.txt` (see [requirements.txt](requirements.txt)).
- Local run: `streamlit run streamlit_app.py`.
- Secrets: the app expects OPENAI_API_KEY in `.env` or Streamlit secrets. See [README.md](README.md) for the `.env` example.
- Windows tip: in PowerShell use `setx OPENAI_API_KEY "your_key"` or create a `.env` and call `load_dotenv()`.

API & integration patterns
- The code uses the modern OpenAI client import pattern: `from openai import OpenAI` and `client = OpenAI(api_key=...)`.
- Calls use the chat completions API: `client.chat.completions.create(...)`. Examples:
  - Non-streaming: model="gpt-4", messages=[...]
  - Streaming: `stream=True` and consumed with `st.write_stream` in `my first chatbot.py`.

Message shape and state
- Session state message lists are used uniformly: a list of dicts with keys `role` and `content`, e.g.:
  - {"role":"system","content":"..."}
  - {"role":"user","content":"..."}
  - {"role":"assistant","content":"..."}
- Two variants appear in the repo: `st.session_state.messages` (my first chatbot.py) and `st.session_state.chat_history` (streamlit_app.py). When changing code, respect the active key used by the file you edit.

Common project-specific guidance
- Prefer [streamlit_app.py](streamlit_app.py) patterns for production behavior (system prompt + session_state + client.chat.completions.create).
- Avoid leaving IPython magic (e.g., `%dotenv`, `%load_text`) in Python scripts — convert them to `from dotenv import load_dotenv` + `load_dotenv()`.
- Use explicit model names found in the repo (`gpt-4`, `gpt-3.5-turbo`).

Editing and testing tips
- To test changes quickly: run `streamlit run streamlit_app.py` and interact in the browser. Check session_state output via temporary `st.write(st.session_state)` if needed.
- If you introduce streaming, mirror the pattern in `my first chatbot.py` using `stream=True` and `st.write_stream`.

Files to inspect for examples
- [streamlit_app.py](streamlit_app.py): compact production example (system prompt, `chat_history`, gpt-4 call).
- [my first chatbot.py](my first chatbot.py): streaming example and `st.secrets` usage.
- [requirements.txt](requirements.txt) and [README.md](README.md): install/run instructions and .env guidance.

What not to assume
- There are no automated tests or CI config in the repo; do not assume test runners are present.
- Notebooks are exploratory; consolidate useful code into `streamlit_app.py` or new modules before refactoring.

When in doubt, ask
- If a choice affects where message state is stored (messages vs chat_history), confirm which UI you intend to update.

End
-- Please review and tell me if you want more details (examples, commands, or CI hooks).
