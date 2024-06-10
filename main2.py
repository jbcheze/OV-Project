import streamlit as st
from dotenv import load_dotenv  # pour charger les clefs api qui sont dans env
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import retrieval_qa
from langchain.chains.question_answering import load_qa_chain
import cohere
import os


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


def summarize_text_with_cohere(
    text,
):  # Objectif : Générer un résumé d'un texte en utilisant l'API Cohere.
    cohere_api_key = os.getenv("API_KEY_COHERE")
    cohere_client = cohere.Client(api_key=cohere_api_key)
    response = cohere_client.generate(
        model="command-xlarge-nightly",
        prompt=f"Summarize this: {text}",
        max_tokens=100,
        temperature=0.5,
    )
    summary = response.generations[0].text.strip()
    return summary


def get_conversation_chain(
    vectorstore,
):  # Objectif : Créer une chaîne de questions-réponses utilisant Cohere et un store vectoriel.
    cohere_api_key = os.getenv("aNQr5ZTkCl5cV76YlLCktgp3xWpTsvMeLgGOCYsN")
    cohere_client = cohere.Client(api_key="aNQr5ZTkCl5cV76YlLCktgp3xWpTsvMeLgGOCYsN")
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    def cohere_chat(prompt):
        response = cohere_client.generate(
            model="command-xlarge-nightly",
            prompt=prompt,
            max_tokens=100,
            temperature=0.5,
        )
        return response.generations[0].text.strip()

    chain = load_qa_chain(
        llm=cohere_chat,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        memory=memory,
    )
    return chain


def main():  # Objectif : Le point d'entrée principal de l'application Streamlit.

    load_dotenv()  # on a mis nos key
    st.set_page_config(page_title="OV-Compromis", page_icon="🏠")
    st.header("Compromis de vente immobilier 🏠")
    question = st.text_input("Posez une question sur le document : ")
    with st.sidebar:
        st.subheader("Vos documents")
        pdf_docs = st.file_uploader(
            "Téléchargez vos PDFs ici et cliquez sur 'Process'",
            accept_multiple_files=True,
        )
        if st.button("Process"):
            with st.spinner("Traitement en cours"):
                # get the pdf text
                raw_text = get_pdf_text(pdf_docs)
                # get the chunk
                text_chunks = get_text_chunks(raw_text)
                # create vector store, embedding = mettre en vecteur pour stocker
                vectorstore = get_vectorstore(text_chunks)
                if vectorstore:
                    st.success("Vectorstore créé avec succès !")
                    # Afficher les vecteurs
                    st.write("Vecteurs générés :", vectorstore)

    with st.container():

        # Generate summaries for each chunk
        summaries = [summarize_text_with_cohere(chunk) for chunk in text_chunks]
        st.subheader("Résumé du document")
        for i, summary in enumerate(summaries):
            st.write(f"Résumé du morceau {i+1}: {summary}")

        conversation = get_conversation_chain(vectorstore)
        if question:
            response = conversation({"question": question})
            st.write(response["answer"])


if __name__ == "__main__":
    main()
