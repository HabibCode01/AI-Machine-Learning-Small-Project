from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.tools import DuckDuckGoSearchRun
import os

# Initialize Web Search Tool
web_search_tool = DuckDuckGoSearchRun()

def get_retriever():
    # Simple setup assuming an existing directory or in-memory instance
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Using an in-memory vector store populated with dummy data for infrastructure
    texts = [
        "Company AI Sdn Bhd specializes in enterprise automation, predictive vision analytics, and LLM deployments.",
        "The internship program at Company AI requires strong proficiency in Python, version control, and API construction.",
        "Production deployment rules dictate that no API secrets should ever be hardcoded into source repositories."
    ]
    
    vectorstore = Chroma.from_texts(texts=texts, embedding=embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 2})

retriever = get_retriever()