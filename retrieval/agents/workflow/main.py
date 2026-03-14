from langgraph.graph import START, StateGraph, END
from retrieval.agents.schemas.models import AgentState
from retrieval.agents.workflow.nodes import retrieve_documents, generate_answer, self_correct
from retrieval.agents.config.settings import MAX_CORRECTION_ITERATIONS
from IPython.display import Image, display
from retrieval.agents.memory.llm_cache import init_llm_cache

init_llm_cache()

def should_continue(state:AgentState) -> str:
    if state.get("iteration",0) >= MAX_CORRECTION_ITERATIONS:
        return END
    return "self_correct"

workflow = StateGraph(AgentState)
workflow.add_node("retrieve_documents", retrieve_documents)
workflow.add_node("generate_answer", generate_answer)
# workflow.add_node("self_correct", self_correct)

workflow.add_edge(START,"retrieve_documents")
workflow.add_edge("retrieve_documents","generate_answer")
workflow.add_edge("generate_answer",END)
# workflow.add_conditional_edges("self_correct", should_continue,
#                              {
#                                   END:END,
#                                   "self_correct":"self_correct"
#                                })
app = workflow.compile()

display(Image(app.get_graph().draw_mermaid_png()))



