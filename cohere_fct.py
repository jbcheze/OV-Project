# from langchain.memory import ConversationBufferMemory
# from langchain.chains import retrieval_qa
from langchain.chains.question_answering import load_qa_chain
from langchain_cohere import ChatCohere


def prompting_draft(text):

    prompting_draft = f"""
    Je souhaite que tu me rédiges un résumé de ce {text} qui sera organisé selon les points suivants:
    - section "Coordonnées du Vendeur et de l'Acquéreur" 
    - section "Bien Immobilier" 
    - section "Hypothèque et servitudes"
    - section "Dossier du Diagnostic Technique (DDT)
    - section "Montant et Modalités de Paiement"
    - section "Durée de Validité de la Promesse de Vente et Date Limite de Signature de l'Acte de Vente Définitif"
    - section "Montant de l’Indemnité d’Immobilisation et Conditions Suspensives"


    Tu rempliras chaque section avec les informations adéquates en organisant ton compte-rendu en bullet points.
    """
    return prompting_draft


def chatting_with_cohere(text, cohere_client):
    response = cohere_client.generate(
        model="command-xlarge-nightly",
        prompt=f"""
    Je souhaite que tu me rédiges un résumé de ce {text} qui sera organisé selon les points suivants:
    - section "Coordonnées du Vendeur et de l'Acquéreur" 
    - section "Bien Immobilier" 
    - section "Hypothèque et servitudes"
    - section "Dossier du Diagnostic Technique (DDT)
    - section "Montant et Modalités de Paiement"
    - section "Durée de Validité de la Promesse de Vente et Date Limite de Signature de l'Acte de Vente Définitif"
    - section "Montant de l'Indemnité d'Immobilisation et Conditions Suspensives"


    Tu rempliras chaque section avec les informations adéquates en organisant ton compte-rendu en bullet points.
    """,
        max_tokens=1000,
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
