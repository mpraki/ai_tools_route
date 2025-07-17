import os
from logging import info

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, ToolMessage, BaseMessage

from .calculator_tool import add, subtract, multiply, divide
from .weather_tool import get_current_temperature
from .wikipedia_tool import search_wikipedia


def answer(question: str) -> dict:
    """Answer a question using the chat model and tools."""
    llm = init_chat_model(model=os.getenv("MODEL"), model_provider=os.getenv("MODEL_PROVIDER"))
    llm_with_tools = llm.bind_tools([get_current_temperature, search_wikipedia, add, subtract, multiply, divide])
    messages: list[BaseMessage] = [HumanMessage(question)]
    ai_msg = llm_with_tools.invoke(messages)
    messages.append(ai_msg)
    for tool_call in ai_msg.tool_calls:
        selected_tool = \
        {"get_current_temperature": get_current_temperature, "search_wikipedia": search_wikipedia, "add": add,
         "subtract": subtract, "multiply": multiply, "divide": divide}[tool_call["name"].lower()]
        tool_output = selected_tool.invoke(tool_call["args"])

        info(f"Tool call: {tool_call['name']} with args: {tool_call['args']}, output: {tool_output}")

        messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))

    result = llm_with_tools.invoke(messages)
    return result.model_dump()
