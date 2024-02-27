import os
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.tools import tool
from langchain_community.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import Chroma, FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.prompts import MessagesPlaceholder, PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from read_file_content import get_file_content


from prompt import (
    prompt_application_summary,
    prompt_qa_with_code,
    prompt_refactor_suggestion,
    prompt_write_testcases )


load_dotenv()

# semicolons_gateway_api_key = os.getenv('semicolons_gateway_api_key')
# semicolons_gateway_base_url = os.getenv('semicolons_gateway_base_url')
# model = os.getenv('model')
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
google_model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.1)
google_model_v1 = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True, temperature=0.1)

embeddings = SentenceTransformerEmbeddings(model_name="paraphrase-MiniLM-L6-v2")
output_parser = StrOutputParser()

zip_text = get_file_content(os.path.join(os.getcwd(),"my_files","test.zip"))

def get_chroma_embeddings():
    raw_documents = TextLoader(os.path.join(os.getcwd(),"my_files","zip_file_text.txt")).load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    documents = text_splitter.split_documents(raw_documents)
    vectordb = Chroma.from_documents(documents=documents, embedding=embeddings)
    return vectordb

def get_FAISS_embeddings(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=10000,
        chunk_overlap=500,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    vectorStore = FAISS.from_texts(texts=chunks, embedding=embeddings)
    return vectorStore


def get_file_content():
    current_dir = os.getcwd()
    uploaded_file_directory = os.path.join(current_dir, "my_files")
    with open(os.path.join(uploaded_file_directory,"zip_file_text.txt"), 'r') as f:
        file_code = f.read()
    return file_code

def get_chatbot_tools():
    file_code = get_file_content()

    def get_tools_response(prompt_text):
        prompt = PromptTemplate.from_template(prompt_text)
        llm_chain = (
                {'context': RunnablePassthrough()}
                | prompt
                | google_model
                | output_parser
        )

        return llm_chain.invoke(file_code)

    @tool
    def get_application_summary(query: str) -> str:

        ''' Use this tool to understand business logic, application summary of the complete application/zip file. '''
        llmresponse = get_tools_response(prompt_application_summary)

        return llmresponse

    @tool
    def get_code_refactoring_suggestions(query: str) -> str:
        ''' Use this tool to extract suggestions for Refactoring, Code Re-usability and code clean up ideas. '''
        llmresponse = get_tools_response(prompt_refactor_suggestion)

        return llmresponse

    @tool
    def write_test_cases(query: str) -> str:
        ''' Use this tool to write test cases for given code base '''
        llmresponse = get_tools_response(prompt_write_testcases)
        return llmresponse

    @tool
    def get_qa_with_code(query: str) -> str:
        ''' Use this tool to for question answering on this code base.
         This tool will extract relevant answer or information from application code base based on User Query '''
        if os.path.exists(os.path.join(os.getcwd(),"my_files","zip_file_text.txt")):

            "Option:1"
            '''get direct response using LLM Chain'''
            llmresponse = get_tools_response(prompt_qa_with_code)

            "Option:2"
            '''get Chroma Vector Store DB and use load_qa_chain'''
            #vectordb = get_chroma_embeddings()
            docs = vectordb.similarity_search(query=query, k=3)
            # chain = load_qa_chain(llm=google_model, chain_type="stuff")
            # llmresponse = chain.run(input_documents=docs, question=query)

            # "Option:3"
            # '''get FAISS Vector Store DB and use load_qa_chain'''
            # vectordb = get_FAISS_embeddings(zip_text)
            # docs = vectordb.similarity_search(query=query)
            # #print('docs:',docs)
            # chain = load_qa_chain(llm=google_model_v1, chain_type="stuff")
            # llmresponse = chain.run(input_documents=docs, question=prompt_qa_with_code)
            # #print(f'llmresponse:{llmresponse}')

            return llmresponse

    return [get_application_summary, get_code_refactoring_suggestions, write_test_cases, get_qa_with_code]

