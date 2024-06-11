import os
import streamlit as st
import cohere
from dotenv import load_dotenv
from pdf_to_vectorstore import get_pdf_text, get_text_chunks, get_vectorstore
from cohere_fct import (
    chatting_with_cohere,
    get_conversation_chain,
    response_to_question,
)


load_dotenv()
cohere_api_key = os.getenv("API_KEY_COHERE")
cohere_client = cohere.Client(api_key=cohere_api_key)


def main():  # Objectif : Le point d'entrée principal de l'application Streamlit.
    st.set_page_config(page_title="OV-Compromis", page_icon=":house:")
    st.header("Compromis de vente immobilier :house:")
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
                # if raw_text:
                #     st.session_state.raw_text = raw_text
                # get the chunk
                text_chunks = get_text_chunks(raw_text)
                # create vector store, embedding = mettre en vecteur pour stocker
                vectorstore = get_vectorstore(text_chunks)
                if vectorstore:
                    st.success("Vectorstore créé avec succès !")
                    st.session_state.vectorstore = vectorstore
                    st.session_state.raw_text = raw_text
                #     # Afficher les vecteurs
                #     st.write("Vecteurs générés :", vectorstore)

    with st.container():
        # Generate summaries for each chunk
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

        st.subheader("Résumé du document")
        texte_complete = raw_text
        summarizing = chatting_with_cohere(texte_complete, cohere_client)
        st.write(summarizing)

        if question:
            vectordb = st.session_state.vectorstore
            answering = response_to_question(question, vectordb, cohere_api_key)
            st.write(answering)


# def main():  # Objectif : Le point d'entrée principal de l'application Streamlit.
#     st.set_page_config(page_title="OV-Compromis", page_icon=":house:")
#     st.header("Compromis de vente immobilier :house:")
#     question = st.text_input("Posez une question sur le document : ")

#     with st.sidebar:
#         st.subheader("Vos documents")
#         pdf_docs = st.file_uploader(
#             "Téléchargez vos PDFs ici et cliquez sur 'Process'",
#             accept_multiple_files=True,
#         )
#         if st.button("Process"):
#             with st.spinner("Traitement en cours"):
#                 # get the pdf text
#                 raw_text = get_pdf_text(pdf_docs)
#                 # get the chunk
#                 text_chunks = get_text_chunks(raw_text)
#                 # create vector store, embedding = mettre en vecteur pour stocker
#                 vectorstore = get_vectorstore(text_chunks)
#                 if vectorstore:
#                     st.success("Vectorstore créé avec succès !")
#                     st.session_state.vectorstore = vectorstore
#                     st.session_state.raw_text = raw_text

#     if "vectorstore" in st.session_state:
#         with st.container():
#             st.subheader("Résumé du document")
#             texte_complete = st.session_state.raw_text
#             summarizing = chatting_with_cohere(texte_complete, cohere_client)
#             st.write(summarizing)

#             if question:
#                 vectordb = st.session_state.vectorstore
#                 answering = response_to_question(question, vectordb, cohere_api_key)
#                 st.write(answering)


if __name__ == "__main__":
    main()
