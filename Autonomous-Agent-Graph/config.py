import os
from dotenv import load_dotenv

# Go up one directory level if needed to find the root .env file
# This loads your GEMINI_API_KEY safely into the background system
load_dotenv(dotenv_path="../.env")

# Set the key into the environment variable that LangChain expects automatically
if os.getenv("GEMINI_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")