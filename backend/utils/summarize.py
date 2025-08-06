from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatMessagePromptTemplate
from dotenv import load_dotenv


load_dotenv()

#Load gemini LLM 
llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    max_tokens = 768,
    temperature=0,
    timeout = None,
    max_retries = 2,
)

#Craft a message 
