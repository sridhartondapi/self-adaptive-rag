from typing import TypedDict, List, Any, Optional
from langchain_core.documents import Document
from pydantic import BaseModel, Field
from langchain_community.retrievers.bm25 import BM25Retriever

class NavigationResponse(BaseModel):
    question: str = Field()
    answer: str = Field()

class AgentState(TypedDict):
    question: str
    answer: str
    response_json: str
    iteration: int
    retrieved_documents: List[Document]
    retrieved_sources: List[str]
    #bm25_retriever: BM25Retriever