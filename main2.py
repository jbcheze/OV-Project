import streamlit as st
from dotenv import load_dotenv  # pour charger les clefs api qui sont dans env
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferMemory
import os

load_dotenv()

cohere_api_key = os.getenv("COHERE_API_KEY")

# Check if the API key is retrieved successfully
if cohere_api_key is None:
    raise ValueError("COHERE_API_KEY not found in environment variables.")
llm = ChatCohere(model="command-r")


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)  # on lit chaque pdf
        for page in pdf_reader.pages:
            text += (
                page.extract_text()
            )  # On extrait le texte des pdf lu et on l'ajoute à text
    return text


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


def get_retriever(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = FAISS.from_documents(
        documents=splits,
        embedding=HuggingFaceBgeEmbeddings(model_name="hkunlp/instructor-xl"),
    )
    # retriever = vectorstore.as_retriever()
    return vectorstore


def pdf_to_vectorstore(pdf_docs):
    # on divise le texte en morceaux de texte pour je pense trouver la réponse du texte à notre question
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)  # on lit chaque pdf
        for page in pdf_reader.pages:
            text += (
                page.extract_text()
            )  # On extrait le texte des pdf lu et on l'ajoute à text
    embeddings = HuggingFaceBgeEmbeddings(model_name="hkunlp/instructor-xl")
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_text(text)
    vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
    return vectorstore


system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "Dis bonjour !"),
    ]
)


def get_conversation_chain(vectorstore):
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vectorstore.as_retriever()
    conversation_chain = create_retrieval_chain(retriever, question_answer_chain)
    return conversation_chain


# def handle_userinput(user_question):
#     response = st.session_state.conversation({'question': user_question})
#     st.session_state.chat_history = response['chat_history']

#     for i, message in enumerate(st.session_state.chat_history):
#         if i % 2 == 0:
#             st.write(user_template.replace(
#                 "{{MSG}}", message.content), unsafe_allow_html=True)
#         else:
#             st.write(bot_template.replace(
#                 "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    load_dotenv()  # on a mis nos key
    st.set_page_config(page_title="OV-Compromis", page_icon="🏠")
    st.header("Compromis de vente immobilier 🏠")
    user_question = st.text_input("Ask a question about your documents:")
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
                st.write(raw_text)
            # get the chunk
            # text_chunks = get_text_chunks(rvectrostoreaw_text)
            # st.write(text_chunks)
            # create vector store, embedding = mettre en vecteur pour stocker
            # vectorstore = get_vectorstore(text_chunks)
            vectorstore = pdf_to_vectorstore(pdf_docs)
            if vectorstore:
                st.success("Vectorstore créé avec succès !")
                retriever = vectorstore.as_retriever()
                st.write(get_conversation_chain(vectorstore))
                print(get_conversation_chain(vectorstore))
                # Afficher les vecteurs
                st.write("Vecteurs générés :", vectorstore)


if __name__ == "__main__":
    main()
