from langchain_community.document_loaders import PyPDFLoader, UnstructuredExcelLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.services.ocr_processor import ocr_processor
import os

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            separators=["\n\n", "\n", " ", ""]
        )

    def process_file(self, file_path: str):
        """
        Processes a file based on its extension.
        If it's a PDF that returns no text, it automatically tries OCR.
        """
        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            # Check if PDF is scanned (empty text)
            content = "".join([d.page_content for d in docs])
            if len(content.strip()) < 50: # Threshold for "scanned" PDF
                text = ocr_processor.scanned_pdf_to_text(file_path)
                from langchain.docstore.document import Document
                docs = [Document(page_content=text, metadata={"source": file_path})]
        elif ext in [".jpg", ".jpeg", ".png"]:
            text = ocr_processor.image_to_text(file_path)
            from langchain.docstore.document import Document
            docs = [Document(page_content=text, metadata={"source": file_path})]
        elif ext in [".xlsx", ".xls"]:
            loader = UnstructuredExcelLoader(file_path)
            docs = loader.load()
        elif ext == ".txt":
            loader = TextLoader(file_path)
            docs = loader.load()
        else:
            raise ValueError(f"Unsupported file extension: {ext}")

        chunks = self.text_splitter.split_documents(docs)
        return chunks

processor = DocumentProcessor()
