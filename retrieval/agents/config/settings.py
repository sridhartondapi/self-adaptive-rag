# app/config/settings.py

import os
from pathlib import Path

# Project root (useful for relative paths)
PROJECT_ROOT = Path(__file__).resolve().parents[3]  

# AWS Bedrock
BEDROCK_REGION = "us-east-1"
LLM_MODEL_ID = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v2:0"

# Vectorstore
VECTORSTORE_PATH = PROJECT_ROOT / ".data" / "chroma_db"

# Memory / Cache
CACHE_DB_PATH = PROJECT_ROOT / "retrieval" / "agents" / "memory" / "langchain_cache.db"

# LangSmith
LANGSMITH_PROJECT = "collegeboard-navigator"

# Retrieval settings
RETRIEVAL_K = 20
MMR_FETCH_K = 80
MMR_LAMBDA_MULT = 0.6
ENSEMBLE_WEIGHTS = [0.75, 0.25]  # semantic, bm25
MAX_DOCS_IN_CONTEXT =5

# Self-correction
MAX_CORRECTION_ITERATIONS = 0

# Any other constants
TEMPERATURE = 0.2
TOP_P = 0.2
MAX_TOKENS = 1024

#collection name
COLLECTION_NAME = "pdf_knowledge_base"