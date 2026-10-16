import os
from dotenv import load_dotenv

load_dotenv()

MODEL = "deepseek-chat"
API_KEY = os.getenv("DEEPSEEK_API_KEY")
