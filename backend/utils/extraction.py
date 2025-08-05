from docling.document_converter import DocumentConverter
from common.sitemap import get_sitemap_urls
converter = DocumentConverter()
source = "C:/Users/DELL/Documents/Personal-Research-Assistant/MyResume.pdf"
doc = converter.convert(source=source).document
result = doc.export_to_markdown()
print(result)