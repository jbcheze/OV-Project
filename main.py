import os
import streamlit as st
import cohere
from dotenv import load_dotenv
from pdf_to_vectorstore import get_pdf_text, get_text_chunks, get_vectorstore
from cohere_fct import chatting_with_cohere, response_to_question, prompting_draft
import base64

load_dotenv()
cohere_api_key = os.getenv("API_KEY_COHERE")
cohere_client = cohere.Client(api_key=cohere_api_key)


def main():  # Objectif : Le point d'entrée principal de l'application Streamlit.
    st.set_page_config(page_title="OV-Compromis", page_icon=":house:")
    mv1 = "images/maison.png"

    with open(mv1, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()

    # Use st.markdown with HTML to control the layout
    st.markdown(
        f"""
        <style>
        .header-container {{
            display: flex;
            align-items: center;
        }}
        .header-text {{
            font-size: 2em;
            margin-right: 10px;  /* Adjust this value to control the space between text and image */
        }}
        .header-image img {{
            width: 50px;
        }}
        </style>
        <div class="header-container">
            <div class="header-text">Compromis de vente immobilier</div>
            <div class="header-image"><img src="data:image/png;base64,{encoded_image}" alt="Maison"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # col1, col2 = st.columns([3, 1], gap="small")
    # with col1:
    #     st.header("Compromis de vente immobilier ")
    # with col2:
    #     st.image(mv1, width=75)

    with st.sidebar:
        img_path = "images/logo_ov2.png"
        st.image(img_path, use_column_width=True)  # width=120
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
            st.subheader("Résumé du document :")
            st.write(st.session_state.summary)

        question = st.text_input("Posez une question sur le document : ")
        if question:
            vectordb = st.session_state.vectorstore
            answering = response_to_question(question, vectordb, cohere_api_key)
            st.write(answering)
    else:
        with st.container(border=True):
            st.subheader("Résumé du document : ")
            st.markdown("<div style='height: 300px;'></div>", unsafe_allow_html=True)
        question = st.text_input("Posez une question sur le document : ")


if __name__ == "__main__":
    main()
