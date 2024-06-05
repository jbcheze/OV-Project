import streamlit as st
from dotenv import load_dotenv #pour charger les clefs api qui sont dans env
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceBgeEmbeddings
#from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.vectorstores import FAISS
import cohere


def get_pdf_text(pdf_docs) :
    text =""
    for pdf in pdf_docs :
        pdf_reader = PdfReader(pdf) # on lit chaque pdf
        for page in pdf_reader.pages : 
            text += page.extract_text() # On extrait le texte des pdf lu et on l'ajoute à text
    return text

def get_text_chunks(text) : #on divise le texte en morceaux de texte pour je pense trouver la réponse du texte à notre question
    text_splitter = CharacterTextSplitter(
    separator = "\n",
    chunk_size = 1000,
    chunk_overlap = 200,
    length_function = len)
    
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks) :
    # embeddings = OpenAIEmbeddings()
    embeddings = HuggingFaceBgeEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts = text_chunks,embeddings=embeddings)
    return vectorstore


def main() : 
    load_dotenv() #on a mis nos key
    st.set_page_config(page_title="OV-Compromis",page_icon="house:")

    st.header("Compromis de vente immobilier:house:")
    st.text_input("Ask a question about the doc : ")

    with st.sidebar :
        st.subheader("Your documments")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on Process",accept_multiple_files=True)
        if st.button("Process") : 
            with st.spinner("Processing") :
                
            # get the pdf text
            
                raw_text = get_pdf_text(pdf_docs)
                #st.write(raw_text)
            
            # get the chunk
            
            text_chunks = get_text_chunks(raw_text)
            st.write(text_chunks)
            
            # create vector store, embedding = mettre en vecteur pour stocker
            
            vectorstore = get_vectorstore(text_chunks)

if __name__ == '__main__' :

    main()
