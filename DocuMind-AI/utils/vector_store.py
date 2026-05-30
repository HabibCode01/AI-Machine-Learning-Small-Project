from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

def create_vector_db(chunks):
    # Use a lightweight, open-source model for local text embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Generate an in-memory vector database from chunks
    vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 3})