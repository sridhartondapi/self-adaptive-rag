from langchain_chroma import Chroma
from langchain_aws import BedrockEmbeddings
from .config import (
    COLLECTION_NAME, 
    CHROMA_PERSIST_DIR, 
    S3_PATH,
    EMBEDDING_MODEL_ID,
    AWS_PROFILE, 
    AWS_REGION
)

import boto3

def get_chroma_client():
    session = boto3.Session(profile_name = AWS_PROFILE)
    bedrock_client = session.client('bedrock-runtime', region_name=AWS_REGION)

    embeddings = BedrockEmbeddings(
        model_id = EMBEDDING_MODEL_ID,
        client = bedrock_client
    )

    chroma_result = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(S3_PATH)
    )

    return chroma_result