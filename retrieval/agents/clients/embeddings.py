from langchain_aws import ChatBedrock, BedrockEmbeddings
from retrieval.agents.clients.bedrock import get_bedrock_client

from retrieval.agents.config.settings import (
    EMBEDDING_MODEL_ID,
)

def get_embeddings():
    bedrock_client = get_bedrock_client()
    return BedrockEmbeddings(
        client=bedrock_client,
        model_id=EMBEDDING_MODEL_ID
    )