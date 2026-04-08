from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    return init_chat_model(
        "claude-haiku-4-5",
        temperature=0.5,
        timeout=10,
        max_tokens=1000
    )