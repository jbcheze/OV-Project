import os
from dotenv import load_dotenv
from langchain_community.llms import VLLMOpenAI
from typing import Any


def load_mistral() -> Any:
    """Load the Mistral language model.

    This function loads environment variables to configure the Mistral language model using the VLLMOpenAI class.
    It sets up the API keys and base URLs required for authentication and returns an instance of the language model
    configured with the specified parameters

    Returns:
        VLLMOpenAI: An instance of the Mistral language model configured with the provided API keys and settings.
    """
    load_dotenv()
    mixtral_api_key = os.getenv("MIXTRAL_API_KEY")
    MIXTRAL_API_BASE = os.getenv("MIXTRAL_API_BASE")

    llm = VLLMOpenAI(
        openai_api_key=mixtral_api_key,
        openai_api_base=MIXTRAL_API_BASE,
        model_name="mistralai/Mixtral-8X7B-Instruct-v0.1",
        temperature=0.0,
        max_tokens=7000,
    )

    return llm
