import os
from dotenv import load_dotenv
import streamlit as st
import shutil

from langchain_openai import ChatOpenAI,AzureChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentType, initialize_agent, AgentExecutor
from langchain.agents.conversational.prompt import SUFFIX
from langchain.prompts import MessagesPlaceholder, PromptTemplate
from langchain.memory import ConversationBufferMemory
from agent_tools import get_chatbot_tools
from langchain.schema import HumanMessage


load_dotenv()

semicolons_gateway_api_key = os.getenv('semicolons_gateway_api_key')
semicolons_gateway_base_url = os.getenv('semicolons_gateway_base_url')
model = os.getenv('model')
openai_deployment_name = os.getenv('deployment_name')
openai_model_name = os.getenv('model_name')
openai_api_version = os.getenv('OPENAI_API_VERSION')
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class CodeChatAgent:

    def __init__(self):
        from prompt import custom_prefix, CUSTOM_FORMAT_INSTRUCTIONS

        llm = ChatOpenAI(
            model_name=model,
            temperature=0.1,
            openai_api_base=semicolons_gateway_base_url,
            openai_api_key=semicolons_gateway_api_key,
        )

        google_model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.1)
        # chatllm = AzureChatOpenAI(
        #     azure_deployment=openai_deployment_name,
        #     openai_api_version=openai_api_version,
        # )
        memory = ConversationBufferMemory(memory_key='chat_history', output_key='output', return_messages=True)
        chat_history = MessagesPlaceholder(variable_name="chat_history")

        ai_prefix: str = "AI"
        tools = get_chatbot_tools()
        custom_prefix = custom_prefix.format(ai_prefix=ai_prefix)

        self.agent = initialize_agent(tools=tools,
                                 llm=google_model, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                                 verbose=True,
                                 system_message=custom_prefix,
                                 handle_parsing_errors=True,
                                 memory=memory, max_iterations=5,
                                 agent_kwargs={
                                  "input_variables": ["input", "chat_history", "agent_scratchpad"],
                                  "output_variables": ["output"],
                              })

    def chat_messages(self,query):
        return self.agent.run(query)



# query = "Write application Summary for given ZIP file."
# CodeChatAgent = CodeChatAgent()
# response = CodeChatAgent.chat_messages(query)
# print(response)

# llm = ChatOpenAI(
#             model_name=model,
#             temperature=0.1,
#             openai_api_base=semicolons_gateway_base_url,
#             openai_api_key=semicolons_gateway_api_key,
#         )
# print(llm.invoke(messages).content)
# #
# # response = llm.invoke("What is capital of INdia")
# # print(response)



