#Deploying Agent to agent A2A with Rag and Fine tuning

#!/usr/bin/env python3
import os
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict
#AGENT TO AGENT COMMUNICATION
from openai import OpenAI
from openai.error import OpenAIError, RateLimitError, APIConnectionError, Timeout, ServiceUnavailableError
#GEMINI API
from google.generativeai import generativeai as gemini
from google.generativeai.errors import GeminiError, RateLimitError as GeminiRateLimitError, ServiceUnavailableError as GeminiServiceUnavailableError
#RETRY LOGIC
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type   
#AGENTS used for agent to agent communication
from langchain.agents import initialize_agent, Tools, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage
from langchain.utilities import GoogleSearchAPIWrapper  
from langchain.agents import create_csv_agent
from langchain.agents import create_pandas_dataframe_agent
from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner
from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor,
from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner
#PANDAS
import pandas as pd
#CSV
import csv
#ENV VARIABLES
from dotenv import load_dotenv
load_dotenv()   
#the two agents will communicate using the LLMs defined below
#logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)    
# Abstract base class for LLM clients
class LLMClient(ABC):
    @abstractmethod
    def generate_text(self, prompt: str, **kwargs) -> str:
        pass
# OpenAI Client
class OpenAIClient(LLMClient):
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        #api key setup
        OpenAI.api_key = self.api_key
        # Retry logic for transient errors
        #retry on specific exceptions with exponential backoff
        #retry up to 5 times with wait time increasing exponentially between 4 and 60 seconds
        #retry decorator from tenacity library
        #wait_exponential for exponential backoff
        #stop_after_attempt to limit the number of retries
        #multiplier, min, and max to control wait time
        #retries if exceptions are raised one or more times 
    @retry(retry=retry_if_exception_type((RateLimitError, APIConnectionError, Timeout, ServiceUnavailableError)),
           wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(5))
    #generate_text implementation for OpenAI
    def generate_text(self, prompt: str, **kwargs) -> str:
        try:
            #call OpenAI API to generate text
            response = OpenAI.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            #return the generated text
            return response.choices[0].message['content'].strip()
        #handle OpenAI specific errors
        #log the error and re-raise it
        except OpenAIError as e:
            #logging the error
            logger.error(f"OpenAI API error: {e}")
            raise
# Gemini Client
class GeminiClient(LLMClient):
    def __init__(self, api_key: str, model: str = "gemini-1.5"):
        self.api_key = api_key
        self.model = model
        gemini.configure(api_key=self.api_key)
    @retry(retry=retry_if_exception_type((GeminiRateLimitError, GeminiServiceUnavailableError)),
           wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(5))
    def generate_text(self, prompt: str, **kwargs) -> str:
        try:
            response = gemini.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.choices[0].message['content'].strip()
        except GeminiError as e:
            logger.error(f"Gemini API error: {e}")
            raise
# Factory to create LLM clients
class LLMClientFactory:
    @staticmethod
    def get_client(provider: str, api_key: str, model: str) -> LLMClient:
        if provider == "openai":
            return OpenAIClient(api_key, model)
        elif provider == "gemini":
            return GeminiClient(api_key, model)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
#to communicate between agents using different LLMs
#starting two agents with different LLMs
#gemini and gpt-4 with RAG and fine tuning to improve performance and accuracy, latency and cost.
# Example usage
if __name__ == "__main__":
    openai_api_key = os.getenv("OPENAI_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    openai_client = LLMClientFactory.get_client("openai", openai_api_key, "gpt-4")
    gemini_client = LLMClientFactory.get_client("gemini", gemini_api_key, "gemini-1.5")
    prompt = "Explain the theory of relativity in simple terms."
    print("OpenAI Response:")
    print(openai_client.generate_text(prompt))
    print("\nGemini Response:")
    print(gemini_client.generate_text(prompt))  
    
# The above code defines a modular system for interacting with different LLM providers (OpenAI and Gemini) using a common interface. 
# It includes robust error handling and retry logic to manage transient API errors.
# The factory pattern is used to instantiate the appropriate client based on the provider name.

#till now they are just LLM clients. Next step is to create agents that use these clients to communicate with each other.
#------------------------------------------------------------------------------
# Agent to Agent Communication (A2A) Example
#!/usr/bin/env python3
import os
from openai import OpenAI
import google.generativeai as genai

#  Setup Clients 
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

#  Agent A: OpenAI (planner/refiner) 
def openai_agent(prompt: str) -> str:
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

#  Agent B: Gemini (researcher/facts) 
def gemini_agent(prompt: str) -> str:
    response = gemini_model.generate_content(prompt)
    return response.text.strip()

#  A2A Communication 
def agent_to_agent(user_question: str) -> str:
    # Step 1: OpenAI decides how to delegate
    planning_prompt = f"""
    You are a planning agent. The user asked: "{user_question}".
    Decide what to ask Gemini (another agent) to gather raw knowledge.
    Just return the exact question you want Gemini to answer.
    """
    query_for_gemini = openai_agent(planning_prompt)

    # Step 2: Gemini answers
    gemini_answer = gemini_agent(query_for_gemini)

    # Step 3: OpenAI refines Gemini's answer into a final response
    refinement_prompt = f"""
    The user asked: "{user_question}".
    Gemini responded with: "{gemini_answer}".
    Please refine this into a clear, accurate, well-structured final answer.
    """
    final_answer = openai_agent(refinement_prompt)

    return final_answer

#  Example Run 
if __name__ == "__main__":
    user_question = "Explain the impact of climate change on global agriculture."
    print("🤖 Final Answer (after A2A collaboration):\n")
    print(agent_to_agent(user_question))
#NOW LETS USE RAG AND FINE TUNING TO IMPROVE PERFORMANCE AND ACCURACY, LATENCY AND COST.
#------------------------------------------------------------------------------
#RAG AND FINE TUNING
#RAG - RETRIEVAL AUGMENTED GENERATION
#FINE TUNING - CUSTOMIZING THE MODEL FOR SPECIFIC TASKS OR DOMAINS
#------------------------------------------------------------------------------
#RAG AND FINE TUNING EXAMPLE
#!/usr/bin/env python3
import os
from langchain import OpenAI, VectorDBQA
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.agents import create_openai_functions_agent
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import CharacterTextSplitter
from langchain.agents import Tools, initialize_agent, AgentType
from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner
import pandas as pd
# Load environment variables
from dotenv import load_dotenv
load_dotenv()   
# Initialize OpenAI model
openai_api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=openai_api_key)
# Load and split documents
def load_and_split_documents(file_path: str):
    loader = TextLoader(file_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    return text_splitter.split_documents(documents)
# Create vector store from documents
def create_vector_store(documents):
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vector_store = FAISS.from_documents(documents, embeddings)
    return vector_store
# Create RetrievalQA chain
def create_retrieval_qa_chain(vector_store):
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    return qa_chain
# Load and prepare documents
documents = load_and_split_documents("sample_docs.txt")
vector_store = create_vector_store(documents)
qa_chain = create_retrieval_qa_chain(vector_store)
# Define tools for the agent
tools = [
    Tools(
        name="DocumentQA",
        func=qa_chain.run,
        description="Useful for answering questions based on the provided documents."
    )
]
# Initialize memory for the agent
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
# Create the agent with planning and execution capabilities
planner = load_chat_planner(llm)
executor = load_agent_executor(llm, tools, agent_type=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, memory=memory)
agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)
# Function to interact with the agent
def ask_agent(question: str) -> str:
    return agent.run(input=question)    
# Example interaction
if __name__ == "__main__":
    user_question = "What are the key benefits of using renewable energy?"
    print("🤖 Agent Response:\n")
    print(ask_agent(user_question))
# The above code demonstrates how to set up a Retrieval-Augmented Generation (RAG) system using LangChain and OpenAI.
# It includes loading documents, creating a vector store for retrieval, and initializing an agent that can
# plan and execute tasks based on user queries, leveraging the provided documents for accurate responses.
# The agent uses a conversational memory to maintain context across interactions.
#------------------------------------------------------------------------------