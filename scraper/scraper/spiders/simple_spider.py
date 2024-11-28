import scrapy
from bs4 import BeautifulSoup
import os

def get_start_urls():
    # urls = os.listdir(os.path.join('/path/to/configMap'))
    urls = ['https://medium.com/@jeff.d.vincent/the-why-and-how-of-sync-and-async-networking-with-microservices-in-python-635b545c3dd7']

    return urls

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
            with open('/Users/jeffvincent/k8s-rag-vectorizor/data/example.txt', 'a') as f:
                f.write(text)
            # self.log(f"Paragraph {i}: {text}")
