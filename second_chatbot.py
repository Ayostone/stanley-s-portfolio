import os
from openai import OpenAI
%load_text dotenv
%dotenv
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
