from retrieval.agents.workflow.main import app
from retrieval.agents.schemas.models import AgentState

question = "show me student data from delaware that started the test but didnt submit and REID"

initial_state = AgentState(
    question= question,
    answer = "",
    retrieved_documents=[],
    retrieved_sources=[],
    iteration=0
)

result = app.invoke(initial_state)

print (result['answer'])
print (f"Iterations: {result['iteration']}")
