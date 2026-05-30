from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_pdf(pdf_path):
    # Load the PDF content
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    # Split the document into chunks of 1000 characters with 200 overlap
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    return chunks