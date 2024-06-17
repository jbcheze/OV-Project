from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings

from langchain.vectorstores import Chroma


def load_split(document_loadded):

    # Load the pdf file and split it into smaller chunks
    loader = PyPDFLoader(document_loadded)
    documents = loader.load()

    # Split the documents into smaller chunks
    text_splitter = CharacterTextSplitter(
        chunk_size=1500, chunk_overlap=0
    )  # Le paramètre chunk_overlap détermine le nombre de caractères qui se chevauchent entre deux segments de texte consécutifs lors du découpage du texte en morceaux (chunks).
    texts = text_splitter.split_documents(documents)

    return texts


def create_retriever(texts):
    # We will use HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings()

    # Using Chroma vector database to store and retrieve embeddings of our text
    db = Chroma.from_documents(
        texts, embeddings
    )  # Creation de la base de donné vectorielle chroma
    retriever = db.as_retriever(
        search_kwargs={"k": 20}
    )  # retriever sert à faire des recherches sémantiques.

    return retriever


# We are using Mistral-7B for this question answering


# We will run an infinite loop to ask questions to LLM and retrieve answers untill the user wants to quit


def question_answer(query, qa_chain):
    chat_history = []
    # while True:
    # query = input("Prompt: ")
    # To exit: use 'exit', 'quit', 'q', or Ctrl-D.",
    # if query.lower() in ["exit", "quit", "q"]:
    # print("Exiting")
    # sys.exit()
    result = qa_chain({"question": query, "chat_history": chat_history})
    print("Answer: " + result["answer"] + "\n")
    chat_history.append((query, result["answer"]))

    return result, chat_history


def summarize(qa_chain):
    prompt = f"""
        Je souhaite que tu me rédiges un résumé du document qui sera organisé selon les points suivants:
        - section "Coordonnées du Vendeur et de l'Acquéreur"
        - section "Bien Immobilier"
        - section "Hypothèque et servitudes"
        - section "Dossier du Diagnostic Technique (DDT ) (mets une phrase sur le DPE en plus)
        - section "Montant et Modalités de Paiement"
        - section "Durée de Validité de la Promesse de Vente et Date Limite de Signature de l'Acte de Vente Définitif"
        - section "Montant de l'Indemnité d'Immobilisation et Conditions Suspensives"
    ,

    Tu rempliras chaque section avec les informations adéquates en organisant ton compte-rendu en bullet points."""

    # prompt = f"- Hypothèque et servitudes"

    chat_history = []

    result = qa_chain({"question": prompt, "chat_history": chat_history})
    return result["answer"]
