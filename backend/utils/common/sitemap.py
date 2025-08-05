import xml.etree.ElementTree as ET
from urllib.parse import urljoin
import requests
from typing import List

def get_sitemap_urls(base_url : str, sitemap_filename : str = "sitemap.xml") -> List[str]:
    try:
        sitemap_url = urljoin(base_url,sitemap_filename)
        response = requests.get(sitemap_url, timeout=10)
        
        if response.status_code == 404:
            raise ValueError("Error 404: Sitemap URL not found.")
        
        response.raise_for_status()
        
         # Parse XML content
        root = ET.fromstring(response.content)
        
         #Handle namespaces
        namespaces = (
            {'ns':root.tag.split("}")[0].strip('{') if "}" in root.tag else ""}
        )
        
        if namespaces:
            urls = [element.text for element in root.findall(".//ns:loc",namespaces=namespaces)]
        else:
            urls = [element.text for element in root.findall(".//loc")]
        
        return urls 
    
    except requests.RequestException as e:
        raise ValueError(f"Failed to fetch sitemap: {str(e)}")
    except ET.ParseError as e:
        raise ValueError(f"Failed to parse sitemap XML: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error processing sitemap: {str(e)}")
        

if __name__ == "__main__":
    print(get_sitemap_urls("https://ds4sd.github.io/docling/"))
    