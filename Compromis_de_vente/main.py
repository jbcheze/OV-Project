import streamlit as st
import base64
from mixtral_loader import load_mistral
from mixtral_chain import create_retriever, question_answer, summarize
from langchain.chains import ConversationalRetrievalChain
from document_loader import upload_file, load_doc
import time

llm = load_mistral()


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
        uploaded_file = upload_file()

        # with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        #     temp_file.write(pdf_docs.read())

        if st.button("Process"):
            if not uploaded_file:
                st.error("Veuillez chargez votre document puis réessayez.")
            else:

                progress_bar = st.progress(0)
                progress_percentage = st.empty()

                # get the pdf text
                if uploaded_file:
                    progress_bar.progress(0)
                    progress_percentage.text("Traitement en cours: 0%")
                    raw_text = load_doc(uploaded_file)
                    progress_bar.progress(25)
                    progress_percentage.text("Traitement en cours: 25%")
                    retriever = create_retriever(raw_text)
                    progress_bar.progress(70)
                    progress_percentage.text("Traitement en cours: 70% ")
                    st.session_state.retriever = retriever

                    qa_chain = ConversationalRetrievalChain.from_llm(
                        llm, retriever, return_source_documents=True
                    )

                    summary = summarize(qa_chain)
                    st.session_state.summary = summary
                    progress_bar.progress(100)
                    progress_percentage.text("Traitement en cours: 100%")
                    time.sleep(0.5)
                    progress_bar.empty()
                    progress_percentage.empty()
                    st.success("Fichier téléchargé avec succès!")

        if st.button("Simulateur de risque"):
            st.switch_page("pages/page2.py")

    if "retriever" in st.session_state:
        with st.container(border=True):
            st.subheader("Résumé du document :")
            st.write(st.session_state.summary)

        question = st.text_input("Posez une question sur le document : ")
        question_template = f"""
        
        N'invente pas de réponse ou tu seras puni
        Si tu ne sais pas, réponds "Non mentionné"
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
            st.subheader("Résumé du document : ")
            st.markdown("<div style='height: 300px;'></div>", unsafe_allow_html=True)
        question = st.text_input("Posez une question sur le document : ")


if __name__ == "__main__":
    main()
