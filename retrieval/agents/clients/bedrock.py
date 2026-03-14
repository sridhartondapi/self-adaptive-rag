import boto3
from langchain_aws import ChatBedrock
from functools import lru_cache

from retrieval.agents.config.settings import (
    BEDROCK_REGION,
    LLM_MODEL_ID,
    TEMPERATURE,
    TOP_P,
    MAX_TOKENS
)

@lru_cache(maxsize=1)
def get_bedrock_client():
    return  boto3.client("bedrock-runtime", region_name=BEDROCK_REGION)

def get_llm():
    client = get_bedrock_client()
    return ChatBedrock(
        client = client,
        model_id= LLM_MODEL_ID,
        model_kwargs = {
            "temperature": TEMPERATURE,
            "top_p":TOP_P,
            "max_tokens": MAX_TOKENS
        }
    )

