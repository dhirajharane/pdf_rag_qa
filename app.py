import streamlit as st
import os
from rag_pipeline import RAGPipeline
from pdf_processor import PDFProcessor
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Streamlit page configuration
st.set_page_config(page_title="PDF Q&A System", page_icon="📚", layout="wide")

def main():
    st.title("📄 PDF Q&A with AI")
    st.markdown("Upload a PDF and ask questions about its content. Powered by RAG and Groq AI.")

    # Initialize session state
    if 'rag_pipeline' not in st.session_state:
        st.session_state.rag_pipeline = None
        st.session_state.pdf_processed = False

    # Check for Groq API key
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        st.error("Groq API key not found. Please set GROQ_API_KEY in the .env file.")
        logger.error("Groq API key missing in .env file")
        return

    # Sidebar for PDF upload
    with st.sidebar:
        st.header("Settings")
        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], help="Upload a PDF file to analyze")

        if uploaded_file:
            try:
                # Save uploaded file temporarily
                with open("temp.pdf", "wb") as f:
                    f.write(uploaded_file.read())
                
                # Process PDF and initialize RAG pipeline
                pdf_processor = PDFProcessor("temp.pdf")
                chunks = pdf_processor.extract_and_chunk()
                
                st.session_state.rag_pipeline = RAGPipeline(chunks, groq_api_key)
                st.session_state.pdf_processed = True
                st.success("PDF processed successfully!")
                logger.info("PDF processed and RAG pipeline initialized")
                
                # Clean up temporary file
                os.remove("temp.pdf")
            except Exception as e:
                st.error(f"Error processing PDF: {str(e)}")
                st.info("If you see an error about 'proxies', try reinstalling dependencies with: `pip install -r requirements.txt --force-reinstall`")
                logger.error(f"PDF processing error: {str(e)}")
                st.session_state.pdf_processed = False

    # Main content area for Q&A
    if st.session_state.pdf_processed:
        st.header("Ask a Question")
        user_question = st.text_input("Your question:", placeholder="e.g., What is the main topic of the document?")
        
        if user_question:
            with st.spinner("Generating answer..."):
                try:
                    answer = st.session_state.rag_pipeline.generate_answer(user_question)
                    st.markdown("### Answer")
                    st.write(answer)
                    logger.info(f"Generated answer for question: {user_question}")
                except Exception as e:
                    st.error(f"Error generating answer: {str(e)}")
                    st.info("If you see an error about 'proxies', try reinstalling dependencies with: `pip install -r requirements.txt --force-reinstall`")
                    logger.error(f"Answer generation error: {str(e)}")
    else:
        st.info("Please upload a PDF to start.")

if __name__ == "__main__":
    main()