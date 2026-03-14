from langchain_classic.retrievers.ensemble import EnsembleRetriever


class RetrievalContext:

    def __init__(self, vectorstore, bm25):
        self.vectorstore = vectorstore
        self.bm25 = bm25

    def hybrid_retrieve(self, query: str, k: int= 50, semantic_weight:float = 0.75):

        semantic = self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs = {
                "k": k,
                "fetch_k": 80,
                "lambda_mult": 0.6
            }
        )

        hybrid = EnsembleRetriever(
                 retrievers=[semantic,self.bm25],
                 weights = [semantic_weight, 1-semantic_weight]
        )

        return hybrid.invoke(query)
    
