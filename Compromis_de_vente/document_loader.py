from langchain_community.document_loaders import PyPDFLoader
from streamlit.runtime.uploaded_file_manager import UploadedFile
from typing import Optional, List
from langchain.schema import Document
from tempfile import NamedTemporaryFile
import streamlit as st


class DocLoader:
    def __init__(self):
        self.pdf_docs = None

    def upload_file(self) -> Optional[str]:
        """Upload and temporarily save a PDF file.

        This function allows users to upload multiple PDF files through a file uploader widget.
        It saves the first uploaded PDF to a temporary file and returns the path to the temporary file.
        If no files are uploaded, it returns None.

        Returns:
            Optional[str]: The path to the temporarily saved PDF file, or None if no files are uploaded.
        """
        self.pdf_docs = st.file_uploader(
            "Téléchargez vos PDFs ici et cliquez sur 'Process'",
            accept_multiple_files=True,
        )
        if not self.pdf_docs:
            return None
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(self.pdf_docs[0].read())
        return temp_file.name

    def load_doc(self, doc_link) -> List[Document]:
        """Load and split a PDF document into smaller chunks.

        This function loads a PDF document from a given file path or link and splits it into smaller
        chunks for easier processing.

        Args:
            doc_link (str): The file path or link to the PDF document.

        Returns:
            list: A list of document chunks extracted from the PDF.
        """
        loader = PyPDFLoader(doc_link)
        documents = loader.load()
        return documents
