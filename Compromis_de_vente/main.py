import streamlit as st
import base64
import time
from mixtral_loader import load_mistral
from mixtral_chain import create_retriever, question_answer, summarize
from langchain.chains import ConversationalRetrievalChain
from document_loader import upload_file, load_doc
from interface import titre, spinner


llm = load_mistral()


def main():  # Objectif : Le point d'entrée principal de l'application Streamlit.
    st.set_page_config(page_title="OV-Compromis", page_icon=":house:")
    mv1 = "images/maison.png"

    with open(mv1, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()

    titre(encoded_image)

    with st.sidebar:
        img_path = "images/logo_ov2.png"
        st.image(img_path, use_column_width=True)
        # st.subheader("Vos documents")

        spinner_style = spinner()

        st.markdown(spinner_style, unsafe_allow_html=True)
        uploaded_file = upload_file()

        if st.button("Process"):
            if not uploaded_file:
                st.error("Veuillez chargez votre document puis réessayez.")
            else:
                loader_placeholder = st.empty()
                progress_bar = st.progress(0)
                progress_percentage = st.empty()

                # get the pdf text
                if uploaded_file:

                    loader_placeholder.markdown(
                        '<div>Traitement en cours: 0%<div id="loader"></div></div>',
                        unsafe_allow_html=True,
                    )
                    progress_bar.progress(0)

                    raw_text = load_doc(uploaded_file)

                    loader_placeholder.markdown(
                        '<div>Traitement en cours: 25%<div id="loader"></div></div>',
                        unsafe_allow_html=True,
                    )
                    progress_bar.progress(25)

                    retriever = create_retriever(raw_text)
                    st.session_state.retriever = retriever

                    loader_placeholder.markdown(
                        '<div>Traitement en cours: 70%<div id="loader"></div></div>',
                        unsafe_allow_html=True,
                    )
                    progress_bar.progress(70)

                    qa_chain = ConversationalRetrievalChain.from_llm(
                        llm, retriever, return_source_documents=True
                    )

                    summary = summarize(qa_chain)
                    st.session_state.summary = summary

                    loader_placeholder.markdown(
                        '<div>Traitement en cours: 100%<div id="loader"></div></div>',
                        unsafe_allow_html=True,
                    )
                    progress_bar.progress(100)
                    time.sleep(0.5)
                    progress_bar.empty()
                    progress_percentage.empty()
                    loader_placeholder.empty()
                    st.success("Fichier téléchargé avec succès!")

        if st.button("Simulateur de risque"):
            st.switch_page("pages/page2.py")

    if "retriever" in st.session_state:
        with st.container(border=True):
            st.subheader("Synthèse :")
            # st.write(st.session_state.summary)
            progressive_summary = ""
            text_placeholder = st.empty()

            for char in st.session_state.summary:
                progressive_summary += (
                    char  # Add the next character to the progressive summary
                )
                text_placeholder.markdown(progressive_summary, unsafe_allow_html=True)
                time.sleep(0.005)

        question = st.text_input("Posez une question sur le document :")

        question_template = f"""

        N'invente pas de réponse ou tu seras puni.
        Si tu ne sais pas, réponds que ce n'est pas mentionné.
        Réponds en français et en te basant seulement et SEULEMENT sur les informations fournies par le document à cette question :
        {question}

        """
        retriever = st.session_state.retriever
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm, retriever, return_source_documents=True
        )
        if question:
            answering = question_answer(question_template, qa_chain)
            st.write(answering)
    else:
        with st.container(border=True):
            st.subheader("Synthèse : ")
            st.markdown("<div style='height: 300px;'></div>", unsafe_allow_html=True)
        question = st.text_input("Posez une question sur le document : ")


if __name__ == "__main__":
    main()
