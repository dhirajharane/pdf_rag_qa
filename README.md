📄 Q & A Generator: PDF Question-Answering System with RAG
A simple web app that lets users upload a PDF, ask questions, and get accurate AI-generated answers using Retrieval-Augmented Generation (RAG). Built to save time for students and professionals by quickly finding information in PDFs.

🌟 Features

Upload any text-based PDF and ask questions about its content.
Uses RAG to retrieve relevant text and generate precise answers.
Fast, free, and easy-to-use interface powered by Streamlit.
Built with open-source tools and the Groq API for answer generation.


🛠️ How It Works

Upload a PDF: Use the Streamlit interface to upload your PDF.
Text Processing: The app extracts text and splits it into chunks using PyPDF2.
Embedding: Chunks are converted into embeddings with Sentence Transformers (all-MiniLM-L6-v2).
Storage & Retrieval: Embeddings are stored in FAISS, which retrieves the top 3 relevant chunks for your question.
Answer Generation: The Groq API (llama3-8b-8192) generates a clear answer based on the chunks.
View Results: The answer is displayed on the web interface in seconds.


📋 Prerequisites

Python 3.9 or higher
A free Groq API key (get it from Groq Console)


🚀 Setup Instructions

Clone the Repository:
git clone https://github.com/yourusername/pdf-qa-generator.git
cd pdf-qa-generator


Create a Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt


Set Up the .env File:

Create a .env file in the project root.
Add your Groq API key:GROQ_API_KEY=your_groq_api_key_here




Run the App:
streamlit run app.py

Open http://localhost:8501 in your browser.



📂 Project Structure

app.py: Main Streamlit app for the web interface and question handling.
pdf_processor.py: Extracts and chunks text from PDFs.
rag_pipeline.py: Manages embeddings, retrieval, and answer generation.
.env: Stores the Groq API key (not included in the repo).
requirements.txt: Lists all dependencies.
README.md: Project documentation (this file).


🖥️ Usage

Open the app in your browser.
Upload a PDF using the sidebar.
Type your question (e.g., "What is the main topic?").
Get a clear, AI-generated answer in seconds!


⚙️ Technologies Used

Streamlit: Web interface
PyPDF2: PDF text extraction
Sentence Transformers: Text embeddings (all-MiniLM-L6-v2)
FAISS: Vector storage and retrieval
Groq API: Answer generation (llama3-8b-8192)
Python-Dotenv: API key management


🐞 Troubleshooting

API Key Error: Ensure your Groq API key is correct in the .env file.
Dependency Issues: Reinstall dependencies with pip install -r requirements.txt --force-reinstall.
PDF Not Processing: The app works with text-based PDFs only (not scanned images).


🌱 Future Improvements

Support for more file types (e.g., Word documents).
Multilingual support for non-English PDFs.
Voice input for asking questions.


👨‍💻 About the Developer
I’m Dhiraj, a second-year Computer Science and Engineering student from Pune, India. I built this project to help students save time while studying from PDFs. Connect with me on GitHub!

📜 License
This project is licensed under the MIT License. Feel free to use and modify it!

Happy Learning! 🚀
