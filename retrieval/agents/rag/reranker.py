import json
from retrieval.agents.clients.bedrock import get_bedrock_client

def bedrock_cohere_rerank(query: str, docs: list, top_n: int=50):
    bedrock = get_bedrock_client()

    doc_texts = [doc.page_content for doc in docs]

    payload = {
        "query": query,
        "documents": doc_texts,
        "top_n": top_n,
        "api_version": 2
    }

    response = bedrock.invoke_model(
        modelId="cohere.rerank-v3-5:0",
        contentType="application/json",
        accept="application/json",
        body=json.dumps(payload).encode("utf-8")
    )

    result = json.loads(response["body"].read().decode("utf-8"))

    reranked_docs = [docs[item["index"]] for item in result["results"]]

    return reranked_docs
