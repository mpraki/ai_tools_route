import os

import panel as pn
import param
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.chat_models import init_chat_model
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_google_genai import GoogleGenerativeAI, ChatGoogleGenerativeAI
from pydantic import SecretStr

from ..tools.calculator_tool import add, subtract, multiply, divide
from ..tools.wikipedia_tool import search_wikipedia
from ..tools.weather_tool import get_current_temperature


class ChatBot(param.Parameterized):

    def __init__(self, **params):
        super(ChatBot, self).__init__(**params)

        tools = [search_wikipedia, get_current_temperature, add, subtract, multiply, divide]

        self.panels = []
        self.model = init_chat_model(model=os.getenv("MODEL"), model_provider=os.getenv("MODEL_PROVIDER"), api_key=SecretStr(os.getenv("GOOGLE_API_KEY")))
        self.model.bind_tools(tools)

        self.memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history")
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are helpful but sassy assistant"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        #self.prompt = hub.pull("hwchase17/openai-functions-agent")
        agent = create_tool_calling_agent(self.model, tools, self.prompt)
        # self.chain = RunnablePassthrough.assign(
        #     agent_scratchpad=lambda x: format_to_openai_functions(x["intermediate_steps"])
        # ) | self.prompt | self.model | OpenAIFunctionsAgentOutputParser()
        self.qa = AgentExecutor(agent=agent, tools=tools, verbose=True, memory=self.memory)

    def convchain(self, query):
        print(f"query: {query}")
        if not query:
            return
        inp.value = ''
        result = self.qa.invoke({"input": query})
        self.answer = result['output']
        self.panels.extend([
            pn.Row('User:', pn.pane.Markdown(query, width=450)),
            pn.Row('ChatBot:', pn.pane.Markdown(self.answer, width=450, styles={'background-color': '#F6F6F6'}))
        ])
        return pn.WidgetBox(*self.panels, scroll=True)

    def run(self):
        global inp
        inp = pn.widgets.TextInput(placeholder='Enter text here…')
        conversation = pn.bind(self.convchain, inp)
        tab1 = pn.Column(
            pn.Row(inp),
            pn.layout.Divider(),
            pn.panel(conversation, loading_indicator=True, height=400),
            pn.layout.Divider(),
        )
        dashboard = pn.Column(
            pn.Row(pn.pane.Markdown('# QnA_Bot')),
            pn.Tabs(('Conversation', tab1))
        )

        pn.serve(dashboard, show=True, verbose=True)
