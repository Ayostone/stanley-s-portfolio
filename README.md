# Darwin Streamlit Chatbot

Setup:

1. Create a `.env` file in the project root with your API key:

```
OPENAI_API_KEY=your_api_key_here
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run streamlit_app.py
```

Notes:
- The app uses the `OpenAI()` client (from the `openai` package) and expects a modern OpenAI SDK.
- If you want streaming responses, I can update `streamlit_app.py` to use the SDK streaming API.
