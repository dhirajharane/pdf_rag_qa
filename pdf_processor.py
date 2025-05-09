import PyPDF2
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PDFProcessor:
    def __init__(self, pdf_path):
        """
        Initialize the PDF processor.
        
        Args:
            pdf_path (str): Path to the PDF file
        """
        self.pdf_path = pdf_path
        logger.info("PDFProcessor initialized for %s", pdf_path)

    def extract_text(self):
        """
        Extract text from the PDF.
        
        Returns:
            str: Extracted text
        """
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                logger.info("Text extracted from PDF: %d characters", len(text))
                return text
        except Exception as e:
            logger.error(f"PDF text extraction error: {str(e)}")
            raise Exception("Failed to extract text from PDF.")

    def chunk_text(self, text, max_chunk_size=500):
        """
        Split text into chunks.
        
        Args:
            text (str): Input text
            max_chunk_size (int): Maximum size of each chunk
        
        Returns:
            list: List of text chunks
        """
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0

        for word in words:
            current_length += len(word) + 1
            if current_length > max_chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = len(word) + 1
            else:
                current_chunk.append(word)
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        logger.info("Text split into %d chunks", len(chunks))
        return chunks

    def extract_and_chunk(self):
        """
        Extract text from PDF and split into chunks.
        
        Returns:
            list: List of text chunks
        """
        text = self.extract_text()
        chunks = self.chunk_text(text)
        return chunks