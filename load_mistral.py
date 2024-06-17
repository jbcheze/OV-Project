import os
from dotenv import load_dotenv
from langchain_community.llms import VLLMOpenAI


def load_mistral():

    load_dotenv()
    mixtral_api_key = os.getenv("MIXTRAL_API_KEY")
    MIXTRAL_API_BASE = os.getenv("MIXTRAL_API_BASE")
    huggingfacehub_api_token = os.getenv("huggingfacehub_api_token")

    llm = VLLMOpenAI(
        openai_api_key=mixtral_api_key,
        openai_api_base=MIXTRAL_API_BASE,
        model_name="mistralai/Mixtral-8X7B-Instruct-v0.1",
        temperature=0.0,
        max_tokens=7000,
    )

    return llm
