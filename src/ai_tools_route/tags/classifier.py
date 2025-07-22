import os
from logging import info

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from pydantic import SecretStr
from .classification import Classification


class Classifier:
    llm = None

    def __init__(self):
        model_name = os.getenv("MODEL")
        model_provider = os.getenv("MODEL_PROVIDER")
        info(f"Initializing Classifier with model: {model_name} and provider: {model_provider}")

        self.llm = init_chat_model(model=model_name, model_provider=model_provider,
                                   api_key=SecretStr(os.getenv("GOOGLE_API_KEY")))

    def classify(self, text: str) -> dict:
        tagging_prompt = ChatPromptTemplate.from_template(
            """
        Extract the desired information from the following passage.
        
        Only extract the properties mentioned in the 'Classification' function.
        
        Passage:
        {input}
        """
        )

        structured_llm = self.llm.with_structured_output(Classification)
        prompt = tagging_prompt.invoke({"input", text})
        return structured_llm.invoke(prompt).model_dump()
