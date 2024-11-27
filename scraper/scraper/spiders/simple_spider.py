import scrapy
from bs4 import BeautifulSoup
import os

def get_start_urls():
    urls = os.listdir(os.path.join('/path/to/configMap'))

class SimpleSpider(scrapy.Spider):
    name = "simple_spider"
    start_urls = get_start_urls()

    def parse(self, response):
        # Parse the response body with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract the title of the page
        title = soup.title.string if soup.title else "No title"
        self.log(f"Page Title: {title}")
        
        # Example: Extract all paragraph texts
        paragraphs = soup.find_all("p")
        for i, p in enumerate(paragraphs, 1):
            text = p.get_text(strip=True)
            self.log(f"Paragraph {i}: {text}")
        
        # Example: Extract all links
        links = soup.find_all("a", href=True)
        for i, link in enumerate(links, 1):
            href = link["href"]
            link_text = link.get_text(strip=True)
            self.log(f"Link {i}: {link_text} ({href})")
        
        # You can save the extracted data, yield it as an item, or perform further processing
