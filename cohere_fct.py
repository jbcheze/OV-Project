# from langchain.memory import ConversationBufferMemory
# from langchain.chains import retrieval_qa
from langchain.chains.question_answering import load_qa_chain
from langchain_cohere import ChatCohere


def chatting_with_cohere(text, cohere_client):
    response = cohere_client.generate(
        model="command-xlarge-nightly",
        prompt=f" Fais un résumé de ce {text} en 7 lignes maximum. Ecris un titre au début et rédige ton paragraphe de façon claire et précise.",
        max_tokens=100,
        temperature=0.5,
    )
    summary = response.generations[0].text.strip()
    return summary


def response_to_question(question, vectorb, cohere_api_key):
    docs = vectorb.similarity_search(question)
    llm = ChatCohere(cohere_api_key=cohere_api_key)
    chain = load_qa_chain(llm, chain_type="stuff")
    ansxer = chain.run(input_documents=docs, question=question)
    return ansxer


# def get_conversation_chain(
#     vectorstore, prompt, cohere_api_key
# ):  # Objectif : Créer une chaîne de questions-réponses utilisant Cohere et un store vectoriel.
#     memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
#     chain = load_qa_chain(
#         llm=ChatCohere(cohere_api_key=cohere_api_key),
#         chain_type="stuff",
#         retriever=vectorstore.as_retriever(),
#         memory=memory,
#     )
#     return chain
