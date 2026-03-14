import os
import requests # type: ignore
from langsmith import traceable, Client
from dotenv import load_dotenv
import certifi
import ssl

trace = traceable

def init_langsmith():
    # Your LangSmith env vars
    load_dotenv()

    # Fix SSL for Python 3.13+ on macOS
    os.environ['SSL_CERT_FILE'] = certifi.where()
    ssl._create_default_https_context = ssl.create_default_context

    print("Env vars set. Key valid?", "lsv2_pt_" in os.environ["LANGSMITH_API_KEY"])

    try:
        response = requests.get("https://api.smith.langchain.com/info", timeout=10)
        print(f"SSL Test: SUCCESS (Status: {response.status_code})")
    except Exception as e:
        print(f"SSL Test FAILED: {e}")

    # Test LangSmith client
    client = Client()
    print("LangSmith Client: READY")
    return client




