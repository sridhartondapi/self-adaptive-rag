from retrieval.agents.rag.vectorstore import get_vectorstore
from retrieval.agents.rag.retrievers import RetrievalContext
from langchain_community.retrievers.bm25 import BM25Retriever

vectorstore = get_vectorstore()

data = vectorstore.get()

bm25 = BM25Retriever.from_texts(
    texts = data['documents'],
    metadatas=data['metadatas']
)

bm25.k = 50

retrieval_ctx = RetrievalContext(
    vectorstore = vectorstore,
    bm25=bm25
)