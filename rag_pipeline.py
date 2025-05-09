from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain_huggingface import HuggingFaceEmbeddings
from groq import Groq
import logging
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self, text_chunks, groq_api_key=None):
        """
        Initialize the RAG pipeline with text chunks and Groq API key.
        
        Args:
            text_chunks (list): List of text chunks from PDF
            groq_api_key (str, optional): Groq API key, defaults to None (loaded from .env)
        """
        if groq_api_key is None:
            groq_api_key = os.getenv("GROQ_API_KEY")
            if not groq_api_key:
                raise ValueError("Groq API key not found in .env file")
        
        try:
            self.groq_client = Groq(api_key=groq_api_key)
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {str(e)}")
            raise Exception("Failed to initialize Groq client. Ensure 'httpx==0.27.2' is installed and check your API key.")
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embedding = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
        self.vector_store = self._create_vector_store(text_chunks)
        logger.info("RAG pipeline initialized")

    def _create_vector_store(self, text_chunks):
        """
        Create a FAISS vector store from text chunks.
        
        Args:
            text_chunks (list): List of text chunks
        
        Returns:
            FAISS: Vector store with embedded chunks
        """
        try:
            documents = [Document(page_content=chunk) for chunk in text_chunks]
            vector_store = FAISS.from_documents(documents, embedding=self.embedding)
            logger.info("Vector store created with %d chunks", len(text_chunks))
            return vector_store
        except Exception as e:
            logger.error(f"Vector store creation error: {str(e)}")
            raise Exception("Failed to create vector store. Ensure all dependencies are correctly installed.")

    def _retrieve_relevant_chunks(self, query, k=3):
        """
        Retrieve top-k relevant chunks for the query.
        
        Args:
            query (str): User question
            k (int): Number of chunks to retrieve
        
        Returns:
            list: Relevant text chunks
        """
        try:
            docs = self.vector_store.similarity_search(query, k=k)
            return [doc.page_content for doc in docs]
        except Exception as e:
            logger.error(f"Retrieval error: {str(e)}")
            raise Exception("Failed to retrieve relevant chunks.")

    def _generate_prompt(self, question, context):
        """
        Generate a prompt for the LLM.
        
        Args:
            question (str): User question
            context (str): Retrieved context
        
        Returns:
            str: Formatted prompt
        """
        prompt = f"""
        You are a helpful AI assistant. Use the following context to answer the question in a detailed, accurate, and coherent manner. Do not indicate what information comes from the context versus your knowledge; provide a single, seamless answer.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """
        return prompt

    def generate_answer(self, question):
        """
        Generate an answer to the user's question using RAG.
        
        Args:
            question (str): User question
        
        Returns:
            str: Generated answer
        """
        # Retrieve relevant chunks
        relevant_chunks = self._retrieve_relevant_chunks(question)
        context = "\n".join(relevant_chunks)
        
        # Generate prompt
        prompt = self._generate_prompt(question, context)
        
        # Call Groq API
        try:
            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            answer = response.choices[0].message.content.strip()
            logger.info("Answer generated successfully")
            return answer
        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            raise Exception("Failed to generate answer. Please check your Groq API key in .env or network connection.")