from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from .extraction import split_into_chunks

load_dotenv()

# Load Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    max_tokens=768,
    temperature=0,
    timeout=None,
    max_retries=2,
)

prompt_template = ChatPromptTemplate(
    [
        ("system", "You are a helpful assistant that summarizes the input given to you."),
        ("human", "{input}")
    ]
)

def summarize_text(text: str) -> str:
    if not text.strip():
        return "[No text to summarize]"

    chunks = split_into_chunks(text)
    summaries = []

    for chunk in chunks:
        chain = prompt_template | llm
        chain_msg = chain.invoke({'input': chunk})
        summaries.append(chain_msg.content)

    combined_summary = '\n\n'.join(summaries)
    final_chain = prompt_template | llm
    final_summary = final_chain.invoke({'input': combined_summary})

    return final_summary.content.strip()
