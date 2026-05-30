from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from app.state import AgentState
from app.tools import retriever, web_search_tool

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0)

def retrieve_node(state: AgentState):
    """Node 1: Retrieve documents from local Vector DB."""
    print("--- RETRIEVING FROM VECTOR STORAGE ---")
    question = state["question"]
    docs = retriever.invoke(question)
    doc_texts = [doc.page_content for doc in docs]
    
    return {"documents": doc_texts, "loop_count": state.get("loop_count", 0) + 1}

def grade_documents_node(state: AgentState):
    """Node 2: Evaluate if retrieved docs match the question intent."""
    print("--- GRADING RELEVANCE OF DOCUMENTS ---")
    question = state["question"]
    docs = state["documents"]
    
    # Prompt the LLM to judge relevance
    combined_docs = "\n".join(docs)
    prompt = f"Analyze if the context is relevant to answer: '{question}'. Context:\n{combined_docs}\nReply with exactly 'YES' or 'NO'."
    
    # Get the raw response from Gemini
    response_msg = llm.invoke([HumanMessage(content=prompt)])
    
    # Safely extract the text, whether Gemini returns a string or a list of thought blocks
    content = response_msg.content
    text_result = content[0].get("text", "") if isinstance(content, list) else content
    
    # Now it is safe to strip and format
    response = str(text_result).strip().upper()
    
    search_needed = True if "NO" in response or not docs else False
    return {"web_search_needed": search_needed}

def web_search_node(state: AgentState):
    """Node 3: Fallback web search node if vector data is insufficient."""
    print("--- EXECUTING FALLBACK WEB SEARCH ---")
    question = state["question"]
    docs = state["documents"]
    
    search_result = web_search_tool.run(question)
    docs.append(f"[Web Result]: {search_result}")
    
    return {"documents": docs}

def generate_node(state: AgentState):
    """Node 4: Synthesize final expert answer."""
    print("--- SYNTHESIZING FINAL RESPONSE ---")
    question = state["question"]
    docs = state["documents"]
    
    context = "\n".join(docs)
    prompt = f"Answer the question accurately using the validated context below.\nContext:\n{context}\nQuestion: {question}"
    
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"generation": response.content}