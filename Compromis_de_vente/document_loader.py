from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from streamlit.runtime.uploaded_file_manager import UploadedFile
from typing import Optional
from tempfile import NamedTemporaryFile
import streamlit as st
import time


def upload_file() -> Optional[str]:
    """_summary_

    Returns:
        Optional[str]: _description_
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
    """_summary_

    Args:
        doc_link (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Load the pdf file and split it into smaller chunks
    loader = PyPDFLoader(doc_link)
    documents = loader.load()

    time.sleep(2)
    return documents
