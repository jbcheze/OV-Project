from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS


def get_pdf_text(pdf_docs):  # Objectif : Lire le texte de plusieurs fichiers PDF.
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)  # on lit chaque pdf
        for page in pdf_reader.pages:
            text += (
                page.extract_text()
            )  # On extrait le texte des pdf lu et on l'ajoute à text
    return text


def get_text_chunks(
    text,
):  # Objectif : Diviser le texte en morceaux plus petits pour faciliter le traitement.
    # on divise le texte en morceaux de texte pour je pense trouver la réponse du texte à notre question
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(
    text_chunks,
):  # Objectif : Créer un store vectoriel pour une recherche sémantique efficace.
    embeddings = HuggingFaceBgeEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore
