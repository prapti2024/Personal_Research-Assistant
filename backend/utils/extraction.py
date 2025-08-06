from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import TokenTextSplitter
from docling.document_converter import DocumentConverter

load_dotenv()

# 1. Load the Gemini LLM
def load_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

# 2. Convert PDF to plain text
def load_pdf_text(filepath: str) -> str:
    converter = DocumentConverter()
    result = converter.convert(filepath)
    return result.document.export_to_text()

# 2.1. Convert URL to plain text
def load_url_text(source: str) -> str:
    converter = DocumentConverter()
    result = converter.convert(source)
    return result.document.export_to_text()


# 3. Split plain text into chunks
def split_into_chunks(text: str, chunk_size=768, chunk_overlap=50) -> list[str]:
    splitter = TokenTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_text(text)



if __name__ == "__main__":
    llm = load_llm()
    pdf_text = load_pdf_text("C:/Users/DELL/Documents/Personal-Research-Assistant/MyResume.pdf")
    chunks = split_into_chunks(pdf_text)

    print(f"Chunks created: {len(chunks)}")
    print(chunks)
