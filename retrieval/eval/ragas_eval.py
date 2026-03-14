# ragas_eval.py
from typing import List, Dict
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
    answer_correctness
)
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from agents.clients.bedrock import get_llm
from agents.clients.embeddings import get_embeddings

# LLM and embeddings wrappers for RAGAS
evaluator_llm = LangchainLLMWrapper(get_llm())
evaluator_embeddings = LangchainEmbeddingsWrapper(get_embeddings())

# Default metrics
DEFAULT_METRICS = [
    faithfulness,
    answer_relevancy,
    answer_correctness,
    context_precision,
    context_recall
]

def run_ragas_eval(dataset: Dataset, metrics=DEFAULT_METRICS) -> List[Dict]:
    """
    Run RAGAS evaluation on a Dataset.
    Returns a list of dictionaries with metric results.
    """
    result = evaluate(
        dataset=dataset,
        metrics=metrics,
        llm=evaluator_llm,
        embeddings=evaluator_embeddings
    )
    return result.to_pandas().to_dict(orient='records')
