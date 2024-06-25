import streamlit as st
import base64
import time
from mixtral_loader import MistralLLM
from mixtral_chain import PDFtoSummary
from document_loader import DocLoader
from interface import Style
from langchain.chains import ConversationalRetrievalChain


interface_instance = Style()
doc_loader_instance = DocLoader()
mixtral_chain_instance = PDFtoSummary()
mistral_instance = MistralLLM()


llm = mistral_instance.load_mistral()


def main() -> None:
    """Main function to orchestrate the application workflow.

    This function sets up the Streamlit page configuration, handles image encoding,
    manages the sidebar with file upload functionality, and processes the uploaded
    file. It also handles displaying the summary of the processed document and
    facilitates question-answering based on the document content.

    Returns:
        Web app streamlit
    """
    logo_OV = "images/V_openvalue.png"

    st.set_page_config(page_title="OV-Compromis", page_icon=logo_OV)
    mv1 = "images/maison_bleu.png"

    with open(mv1, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()

    interface_instance.titre(encoded_image, "Compromis de Vente Immobilier")

    with st.sidebar:
        img_path = "images/logo_ov2.png"
        st.image(img_path, use_column_width=True)

        spinner_style = interface_instance.spinner()

        st.markdown(spinner_style, unsafe_allow_html=True)
        uploaded_file = doc_loader_instance.upload_file()

        if st.button("Process"):
            if not uploaded_file:
                st.error("Veuillez chargez votre document puis réessayez.")
            else:
                loader_placeholder = st.empty()
                progress_bar = st.progress(0)
                progress_percentage = st.empty()

                if uploaded_file:

                    loader_placeholder.markdown(
                        '<div>Traitement en cours: 0%<div id="loader"></div></div>',
                        unsafe_allow_html=True,
                    )
                    progress_bar.progress(0)

                    raw_text = doc_loader_instance.load_doc(uploaded_file)

                    loader_placeholder.markdown(
                        '<div>Traitement en cours: 25%<div id="loader"></div></div>',
                        unsafe_allow_html=True,
                    )
                    progress_bar.progress(25)

                    retriever = mixtral_chain_instance.create_retriever(raw_text)
                    st.session_state.retriever = retriever

                    loader_placeholder.markdown(
                        '<div>Traitement en cours: 70%<div id="loader"></div></div>',
                        unsafe_allow_html=True,
                    )
                    progress_bar.progress(70)

                    qa_chain = ConversationalRetrievalChain.from_llm(
                        llm, retriever, return_source_documents=True
                    )

                    summary = mixtral_chain_instance.summarize(qa_chain)
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

    if "retriever" in st.session_state:
        if "summary_by_char" not in st.session_state:
            with st.container(border=True):
                st.subheader("Synthèse :")
                progressive_summary = ""
                text_placeholder = st.empty()

                for char in st.session_state.summary:
                    progressive_summary += char
                    text_placeholder.markdown(
                        progressive_summary, unsafe_allow_html=True
                    )
                    time.sleep(0.005)
            st.session_state.summary_by_char = st.session_state.summary
        else:
            with st.container(border=True):
                st.subheader("Synthèse :")
                st.write(st.session_state.summary)
        question = st.text_input("Posez une question sur le document : ")
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
            answering = mixtral_chain_instance.question_answer(
                question_template, qa_chain
            )
            st.write(answering)
    else:
        with st.container(border=True):
            st.subheader("Synthèse : ")
            st.markdown(
                "<div  style='height: 300px;'></div>",
                unsafe_allow_html=True,
            )
        question = st.text_input("Posez une question sur le document : ")


if __name__ == "__main__":
    main()
