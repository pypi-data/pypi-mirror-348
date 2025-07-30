import fitz  # PyMuPDF

class Transformations:
    @staticmethod
    def chunk_text_manual(text, chunk_size=1000, overlap=200):
        """
        Splits text into overlapping chunks.
        :param text: The input string to chunk.
        :param chunk_size: The size of each chunk.
        :param overlap: The number of overlapping characters between chunks.
        :return: List of text chunks.
        """
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks

    @staticmethod
    def extract_text_from_pdf(file_bytes):
        """
        Extracts text from PDF bytes using PyMuPDF (fitz).
        :param file_bytes: PDF file content as bytes.
        :return: Extracted text as a string.
        """
        text = ""
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()
