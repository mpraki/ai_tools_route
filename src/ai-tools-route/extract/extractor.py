import os
from logging import info

from extract.person import People
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from pydantic import SecretStr


class Extractor:
    llm = None

    def __init__(self):
        model_name = os.getenv("MODEL")
        model_provider = os.getenv("MODEL_PROVIDER")
        info(f"Initializing Extractor with model: {model_name} and provider: {model_provider}")

        self.llm = init_chat_model(model=model_name, model_provider=model_provider,
                                   api_key=SecretStr(os.getenv("GOOGLE_API_KEY")))

    def extract(self, text: str) -> dict:
        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert extraction algorithm. "
                    "Only extract relevant information from the text. "
                    "If you do not know the value of an attribute asked to extract, "
                    "return null for the attribute's value.",
                ),
                ("human", "{text}"),
            ]
        )

        structured_llm = self.llm.with_structured_output(People)
        prompt = prompt_template.invoke({"text": text})
        return structured_llm.invoke(prompt).model_dump()
