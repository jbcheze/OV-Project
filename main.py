import os
import streamlit as st
<<<<<<< HEAD
import cohere
from dotenv import load_dotenv
from pdf_to_vectorstore import get_pdf_text, get_text_chunks, get_vectorstore
from cohere_fct import (
    summarize_text_with_cohere,
    chatting_with_cohere,
    get_conversation_chain,
    response_to_question,
)
=======
from dotenv import load_dotenv  # pour charger les clefs api qui sont dans env
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import retrieval_qa
from langchain.llms import openai
from openai import OpenAI
from langchain.chains.retrieval import create_retrieval_chain
>>>>>>> 05946453901369950fe60ec83a92bbf8ba3365fe


load_dotenv()
cohere_api_key = os.getenv("API_KEY_COHERE")
cohere_client = cohere.Client(api_key=cohere_api_key)


<<<<<<< HEAD
def main():  # Objectif : Le point d'entrée principal de l'application Streamlit.
    st.set_page_config(page_title="OV-Compromis", page_icon=":house:")
    st.header("Compromis de vente immobilier :house:")
    question = st.text_input("Posez une question sur le document : ")
=======
def get_text_chunks(text):
    # on divise le texte en morceaux de texte pour je pense trouver la réponse du texte à notre question
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    # embeddings = OpenAIEmbeddings()
    embeddings = HuggingFaceBgeEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = OpenAI()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


def main():
    load_dotenv()  # on a mis nos key
    st.set_page_config(page_title="OV-Compromis", page_icon="🏠")
    st.header("Compromis de vente immobilier 🏠")
    st.text_input("Posez une question sur le document : ")
>>>>>>> 05946453901369950fe60ec83a92bbf8ba3365fe
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
<<<<<<< HEAD
                # get the chunk
                text_chunks = get_text_chunks(raw_text)
                # create vector store, embedding = mettre en vecteur pour stocker
                vectorstore = get_vectorstore(text_chunks)
                if vectorstore:
                    st.success("Vectorstore créé avec succès !")
                    st.session_state.vectorstore = vectorstore
                #     # Afficher les vecteurs
                #     st.write("Vecteurs générés :", vectorstore)

    with st.container():
        # # Generate summaries for each chunk
        # summaries = [
        #     summarize_text_with_cohere(chunk, cohere_client) for chunk in text_chunks
        # ]
        # st.subheader("Résumé du document")
        # for i, summary in enumerate(summaries):
        #     st.write(f"Résumé du morceau {i+1}: {summary}")
        # conversation = get_conversation_chain(vectorstore, "bonjour", cohere_api_key)
        # if question:
        #     response = conversation({"question": question})
        #     st.write(response["answer"])

        if question:
            vectordb = st.session_state.vectorstore
            answering = response_to_question(question, vectordb, cohere_api_key)
            st.write(answering)
=======
                # st.write(raw_text)
            # get the chunk
            text_chunks = get_text_chunks(raw_text)
            # st.write(text_chunks)
            # create vector store, embedding = mettre en vecteur pour stocker
            vectorstore = get_vectorstore(text_chunks)
            if vectorstore:
                st.success("Vectorstore créé avec succès !")
                # Afficher les vecteurs
                st.write("Vecteurs générés :", vectorstore)

            conversation = get_conversation_chain(vectorstore)
>>>>>>> 05946453901369950fe60ec83a92bbf8ba3365fe


if __name__ == "__main__":
    main()
