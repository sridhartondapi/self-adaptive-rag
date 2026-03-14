from dotenv import load_dotenv
import os, boto3

load_dotenv()

DOCUMENT_DIR = "./ingestion/source/reports"  
CHROMA_PERSIST_DIR = os.getenv("INDEX_PATH","data/chroma_db")

S3_BUCKET = "hybrid-rag-linear-flow"   
S3_PREFIX = "chroma_db/"
S3_PATH = CHROMA_PERSIST_DIR        


HASH_FILE = os.path.join(CHROMA_PERSIST_DIR,".processed_hashes.json")

AWS_PROFILE = os.getenv("AWS_PROFILE", "default")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
EMBEDDING_MODEL_ID = os.getenv("EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE","300"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP","200"))

COLLECTION_NAME = "pdf_knowledge_base"

s3_client = boto3.Session(profile_name=AWS_PROFILE).client('s3')
