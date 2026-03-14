from langsmith import trace
from retrieval.agents.schemas.models import AgentState
from retrieval.agents.workflow.graph import retrieval_ctx
from retrieval.agents.rag.reranker import bedrock_cohere_rerank
from retrieval.agents.clients.bedrock import get_llm
from retrieval.agents.config.settings import MAX_CORRECTION_ITERATIONS, MAX_DOCS_IN_CONTEXT
from retrieval.agents.schemas.models import NavigationResponse
from retrieval.agents.config.prompts import custom_prompt, correction_prompt
from retrieval.agents.memory.llm_cache import init_llm_cache


init_llm_cache()
llm = get_llm()


def retrieve_documents(state:AgentState) -> AgentState:
    with trace("retrieve_documents"):
        query = state['question']
        docs = retrieval_ctx.hybrid_retrieve(query)
        reranked_docs = bedrock_cohere_rerank(query, docs)
        state['retrieved_documents'] = reranked_docs
        state['retrieved_sources'] = [ doc.metadata.get("sources","unknown") for doc in reranked_docs]
        return state


def generate_answer(state:AgentState) -> AgentState:
    with trace("generate_answer"):
        question = state['question']
        
        docs_to_text_lines = "\n\n".join(doc.page_content for doc in state['retrieved_documents'][:MAX_DOCS_IN_CONTEXT])
        initial_answer = custom_prompt.format(question=question, context=docs_to_text_lines)

        response = llm.invoke(initial_answer).content
        structured = NavigationResponse(
            question=question, 
            answer=response
            )
        state['answer'] = structured.answer
        state['retrieved_sources'] = state.get('retrieved_sources', [])
        state['response_json'] = structured.model_dump_json(indent=2)
        return state


def self_correct(state:AgentState) -> AgentState:
    with trace("self_correct"):
        answer = state['answer']
        question = state['question']
        docs = state['retrieved_documents']

        try:
            correction_output = correction_prompt.format(question=question, answer=answer, docs=docs)
            correction_result = llm.invoke(correction_output).content.strip()

            if correction_result == 'ACCEPT':
                return {
                    **state, 
                    "iteration": state.get("iteration",0)+1 , 
                    "answer":answer,
                    "response_json": state.get("response_json")
                        }
            structured = NavigationResponse(
                question = question,
                answer = correction_result
                                            )
            return {
                **state, 
                "iteration": state.get("iteration", 0)+1, 
                "answer": correction_result,
                "response_json": structured.model_dump_json(indent=2)
                }
        except Exception as e:
            print (f"Error in the self correction node: {str(e)}")
            return state


