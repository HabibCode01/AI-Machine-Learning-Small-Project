import config  # Ensure environment variables load first
from langgraph.graph import StateGraph, END
from app.state import AgentState
from app.nodes import retrieve_node, grade_documents_node, web_search_node, generate_node

# 1. Initialize State Graph
workflow = StateGraph(AgentState)

# 2. Add System Workspace Nodes
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("grade_documents", grade_documents_node)
workflow.add_node("web_search", web_search_node)
workflow.add_node("generate", generate_node)

# 3. Establish Core Workflows (Edges)
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "grade_documents")

# 4. Define Router Logic (Conditional Edges)
def decide_next_step(state: AgentState):
    # Added .get() for safety in case loop_count hasn't initialized yet
    if state["web_search_needed"] and state.get("loop_count", 0) < 2:
        print("--- ROUTING STATUS: DATA INSUFFICIENT -> FORWARDING TO WEB ---")
        return "web_search"
    else:
        print("--- ROUTING STATUS: DATA VALIDATED -> GENERATING RESPONSE ---")
        return "generate"

workflow.add_conditional_edges(
    "grade_documents",
    decide_next_step,
    {
        "web_search": "web_search",
        "generate": "generate"
    }
)

workflow.add_edge("web_search", "generate")
workflow.add_edge("generate", END)

# 5. Compile the Runnable Application Graph
app_graph = workflow.compile()

# --- VISUALIZATION PIPELINE ---
# Print the visual structure to the terminal
print("\n--- AGENTIC WORKFLOW GRAPH ---")
app_graph.get_graph().print_ascii()
print("------------------------------\n")

# Save the graph as a high-quality PNG image using Mermaid
with open("agent_architecture.png", "wb") as f:
    f.write(app_graph.get_graph().draw_mermaid_png())
print("✅ Graph architecture saved as 'agent_architecture.png' in your project folder!\n")
# ------------------------------

if __name__ == "__main__":
    print("\n🚀 Testing Case 1: Internal Knowledge Query (Should use local Vector store)")
    inputs = {"question": "What does Imagine AI specialize in?"}
    for output in app_graph.stream(inputs):
        pass
    print(f"\nFinal Result:\n{output.get('generate', {}).get('generation', 'No result generated.')}\n")
    
    print("-" * 50)
    
    print("\n🚀 Testing Case 2: Unknown Out-of-Domain Query (Should trigger routing to web fallback)")
    inputs_out = {"question": "What is the capital city of France?"}
    for output_out in app_graph.stream(inputs_out):
        pass
    print(f"\nFinal Result:\n{output_out.get('generate', {}).get('generation', 'No result generated.')}")