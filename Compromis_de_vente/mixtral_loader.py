import os
from dotenv import load_dotenv
from langchain_community.llms import VLLMOpenAI
from typing import Any


class MistralLLM:
    def __init__(self):
        """Initialise les variables d'environnement nécessaires pour le modèle."""
        load_dotenv()
        self.mixtral_api_key = os.getenv("MIXTRAL_API_KEY")
        self.mixtral_api_base = os.getenv("MIXTRAL_API_BASE")
        self.model_name = "mistralai/Mixtral-8X7B-Instruct-v0.1"
        self.temperature = 0.0
        self.max_tokens = 7000

    def load_mistral(self) -> Any:
        """Charge le modèle de langage Mistral avec les paramètres configurés.

        Returns:
            VLLMOpenAI: Une instance du modèle de langage Mistral configuré.
        """
        llm = VLLMOpenAI(
            openai_api_key=self.mixtral_api_key,
            openai_api_base=self.mixtral_api_base,
            model_name=self.model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return llm
