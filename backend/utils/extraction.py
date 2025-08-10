from langchain.text_splitter import TokenTextSplitter
from docling.document_converter import DocumentConverter

# Convert PDF to plain text
def load_pdf_text(filepath: str) -> str:
    converter = DocumentConverter()
    result = converter.convert(filepath)
    text =  result.document.export_to_text()
    print(f"[DEBUG] Extracted text length: {len(text)}")
    return text

def extract_text_from_url(url:str) -> str:
    converter = DocumentConverter()
    result = converter.convert(url)
    return result.document.export_to_text()
    

#  Split plain text into chunks
def split_into_chunks(text: str, chunk_size=768, chunk_overlap=50) -> list[str]:
    splitter = TokenTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_text(text)

if __name__ == "__main__":
  pdf_text = load_pdf_text("C:/Users/DELL/Documents/Personal-Research-Assistant/MyResume.pdf")
  chunks = split_into_chunks(pdf_text)
  print(f"Chunks created: {len(chunks)}")
  print(chunks)
