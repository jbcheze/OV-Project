from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

import time


def create_retriever(pdf_loaded):
    """_summary_

    Args:
        pdf_loaded (_type_): _description_

    Returns:
        _type_: _description_
    """
    text_splitter = CharacterTextSplitter(
        chunk_size=2000, chunk_overlap=250
    )  # Le paramètre chunk_overlap détermine le nombre de caractères qui se chevauchent entre deux segments de texte consécutifs lors du découpage du texte en morceaux (chunks).
    texts = text_splitter.split_documents(pdf_loaded)

    # We will use HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings()

    # Using Chroma vector database to store and retrieve embeddings of our text
    db = Chroma.from_documents(
        texts, embeddings
    )  # Creation de la base de donné vectorielle chroma
    retriever = db.as_retriever(
        search_kwargs={"k": 20}
    )  # retriever sert à faire des recherches sémantiques.

    time.sleep(2)
    return retriever


def question_answer(query, qa_chain):
    """_summary_

    Args:
        query (_type_): _description_
        qa_chain (_type_): _description_

    Returns:
        _type_: _description_
    """
    chat_history = []
    # while True:
    # query = input("Prompt: ")
    # To exit: use 'exit', 'quit', 'q', or Ctrl-D.",
    # if query.lower() in ["exit", "quit", "q"]:
    # print("Exiting")
    # sys.exit()
    result = qa_chain({"question": query, "chat_history": chat_history})
    print("Answer: " + result["answer"] + "\n")

    return result["answer"]


def summarize(qa_chain):
    """_summary_

    Args:
        qa_chain (_type_): _description_

    Returns:
        _type_: _description_
    """

    prompt = f"""
        Je souhaite que tu me rédiges un résumé du document qui sera organisé selon les points suivants:
        - section "Coordonnées du Vendeur et de l'Acquéreur"
        - section "Bien Immobilier"
        - section "Hypothèque et servitudes"
        - section "Dossier du Diagnostic Technique (DDT)"
        - section "Diagnostics de Performance Energetique (DPE)",(en parlant seulement des classes)
        - section "Montant et Modalités de Paiement"
        - section "Durée de Validité de la Promesse de Vente et Date Limite de Signature de l'Acte de Vente Définitif"
        - section "Montant de l'Indemnité d'Immobilisation et Conditions Suspensives"
    ,

    Tu rempliras chaque section avec les informations adéquates en organisant ton compte-rendu en bullet points."""

    # prompt = f"- Hypothèque et servitudes"

    chat_history = []

    result = qa_chain({"question": prompt, "chat_history": chat_history})

    time.sleep(2)
    return result["answer"]
