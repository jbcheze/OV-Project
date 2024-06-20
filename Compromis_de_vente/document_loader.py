from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from streamlit.runtime.uploaded_file_manager import UploadedFile
from typing import Optional
from tempfile import NamedTemporaryFile
import streamlit as st
import time


def upload_file() -> Optional[str]:
    """Upload and temporarily save a PDF file.

    This function allows users to upload multiple PDF files through a file uploader widget.
    It saves the first uploaded PDF to a temporary file and returns the path to the temporary file.
    If no files are uploaded, it returns None.

    Returns:
        Optional[str]: The path to the temporarily saved PDF file, or None if no files are uploaded.
    """
    pdf_docs: Optional[list[UploadedFile]] = st.file_uploader(
        "Téléchargez vos PDFs ici et cliquez sur 'Process'",
        accept_multiple_files=True,
    )
    if not pdf_docs:
        return None
    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(pdf_docs[0].read())
    return temp_file.name


def load_doc(doc_link):
    """Load and split a PDF document into smaller chunks.

    This function loads a PDF document from a given file path or link and splits it into smaller
    chunks for easier processing.

    Args:
        doc_link (str): The file path or link to the PDF document.

    Returns:
        list: A list of document chunks extracted from the PDF.
    """
    # Load the pdf file and split it into smaller chunks
    loader = PyPDFLoader(doc_link)
    documents = loader.load()

    time.sleep(2)
    return documents
