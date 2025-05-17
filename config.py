import os

from dotenv import load_dotenv

load_dotenv()

SEARCH_TERM = "python"
MAX_JOBS = 25
OUTPUT_DIR = "outputs"
IDS_FILE = "job_ids.txt"

WAIT_INITIAL = 8
WAIT_SCROLL = 3

# GPT Config
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GPT_MODEL = "gpt-4o"
GPT_MAX_TOKENS = 800
GPT_TEMPERATURE = 0.3
