import os
import streamlit as st
import cohere
from dotenv import load_dotenv
from pdf_to_vectorstore import get_pdf_text, get_text_chunks, get_vectorstore
from cohere_fct import (
    chatting_with_cohere,
    response_to_question,
)


load_dotenv()
cohere_api_key = os.getenv("API_KEY_COHERE")
cohere_client = cohere.Client(api_key=cohere_api_key)


def main():  # Objectif : Le point d'entrée principal de l'application Streamlit.
    st.set_page_config(page_title="OV-Compromis", page_icon=":house:")
    st.header("Compromis de vente immobilier :house:")
    with st.sidebar:
        img_path = "images/logo_ov2.png"
        st.image(img_path, use_column_width=True)
        st.subheader("Vos documents")
        pdf_docs = st.file_uploader(
            "Téléchargez vos PDFs ici et cliquez sur 'Process'",
            accept_multiple_files=True,
        )

        if st.button("Process"):
            with st.spinner("Traitement en cours"):
                # get the pdf text
                raw_text = get_pdf_text(pdf_docs)
                summary = chatting_with_cohere(raw_text, cohere_client)
                st.session_state.summary = summary
                # get the chunk
                text_chunks = get_text_chunks(raw_text)
                # create vector store, embedding = mettre en vecteur pour stocker
                vectorstore = get_vectorstore(text_chunks)
                if vectorstore:
                    st.success("Document téléchargé avec succès !")
                    st.session_state.vectorstore = vectorstore

    if "vectorstore" in st.session_state:
        with st.container(border=True):
            st.subheader("Résumé du document")
            st.write(st.session_state.summary)

        question = st.text_input("Posez une question sur le document : ")
        if question:
            vectordb = st.session_state.vectorstore
            answering = response_to_question(question, vectordb, cohere_api_key)
            st.write(answering)
    else:
        with st.container(border=True):
            st.subheader("Résumé du document ")
            st.markdown("<div style='height: 300px;'></div>", unsafe_allow_html=True)
        question = st.text_input("Posez une question sur le document : ")


if __name__ == "__main__":
    main()
