import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv  # Fixed typo here
from utils.pdf_processor import process_pdf
from utils.vector_store import create_vector_db

# Load variables from .env file
load_dotenv()

# Retrieve the key securely
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

st.set_page_config(page_title="DocuMind AI", layout="centered")
st.title("📄 DocuMind AI - RAG Document Search")

uploaded_file = st.file_uploader("Upload your document (PDF)", type=["pdf"])

if uploaded_file:
    temp_path = "temp_doc.pdf"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    st.success("Document uploaded successfully! Indexing text...")
    
    # Process text chunks and build retriever pipeline
    chunks = process_pdf(temp_path)
    retriever = create_vector_db(chunks)
    
    query = st.text_input("Ask a question about this document:")
    if query:
        # Retrieve the top 3 matching chunks
        relevant_docs = retriever.invoke(query)
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        # Build strict system context prompt
        prompt = f"System: Answer the query based ONLY on the context below.\n\nContext:\n{context}\n\nQuery: {query}"
        
        model = genai.GenerativeModel('gemini-3.5-flash')
        response = model.generate_content(prompt)
        
        st.write("### AI Response:")
        st.write(response.text)
        
    # Clean up local file after execution
    if os.path.exists(temp_path):
        os.remove(temp_path)