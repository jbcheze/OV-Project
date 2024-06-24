from langchain.text_splitter import (
    CharacterTextSplitter,
)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.vectorstores import VectorStoreRetriever
from typing import List
import time


def create_retriever(pdf_loaded) -> VectorStoreRetriever:
    """Create a retriever for semantic search from loaded PDF documents.

    This function splits the text of the loaded PDF documents into chunks, generates embeddings
    for these chunks using HuggingFace embeddings, and stores them in a Chroma vector database.
    It then creates and returns a retriever for performing semantic searches on these embeddings.

    Args:
        pdf_loaded (list): A list of loaded PDF documents to be processed.

    Returns:
        ChromaRetriever: A retriever object for performing semantic searches on the document embeddings.
    """
    text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=250)
    texts = text_splitter.split_documents(pdf_loaded)

    embeddings = HuggingFaceEmbeddings()

    db = Chroma.from_documents(texts, embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 20})

    time.sleep(2)
    return retriever


def question_answer(query, qa_chain) -> str:
    """Get an answer to a query using a question-answering chain.

    This function takes a query and a question-answering chain object, processes the query to obtain an answer,
    and prints the answer. The chat history is maintained for context.

    Args:
        query (str): The query or question to be answered.
        qa_chain (function): The question-answering chain function that processes the query.

    Returns:
        str: The answer to the query.
    """
    chat_history: List = []
    result = qa_chain({"question": query, "chat_history": chat_history})
    print("Answer: " + result["answer"] + "\n")

    return result["answer"]


def summarize(qa_chain) -> str:
    """Generate a summary of a document organized by specific sections.

    This function generates a summary of a document based on a predefined template with specific sections.
    It uses a question-answering chain to process the prompt and extract the relevant information
    for each section. The summary is organized in bullet points.

    Args:
        qa_chain (function): The question-answering chain function that processes the prompt.

    Returns:
        str: The summarized document organized by sections.
    """

    prompt = f"""
        Je suis un agent immobilier et je travaille sur des compromis de vente 
        Je souhaite que tu me rédiges un résumé du document qui sera organisé selon les points suivants:
        - section "Coordonnées du Vendeur et de l'Acquéreur"
        - section "Bien Immobilier"
        - section "Hypothèque et servitudes"
        - section "Dossier du Diagnostic Technique (DDT)"
        - section "Diagnostics de Performance Energetique (DPE)",(en parlant seulement des classes)
        - section "Montant et Modalités de Paiement"
        - section "Date de Signature de l'Acte de Vente"
        - section "Montant de l'Indemnité d'Immobilisation et Conditions Suspensives"
    ,

    Tu rempliras chaque section avec les informations adéquates en organisant ton compte-rendu en bullet points."""

    chat_history: List = []
    result = qa_chain({"question": prompt, "chat_history": chat_history})
    time.sleep(2)
    return result["answer"]
