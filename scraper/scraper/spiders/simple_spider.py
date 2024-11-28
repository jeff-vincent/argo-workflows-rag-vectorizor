import scrapy
from bs4 import BeautifulSoup
import os

def get_start_urls():
    # urls = os.listdir(os.path.join('/path/to/configMap'))
    urls = ['https://www.mongodb.com/docs/atlas/tutorial/connect-to-your-cluster/']

    return urls

class SimpleSpider(scrapy.Spider):
    name = "simple_spider"
    start_urls = get_start_urls()

    def parse(self, response):
        # Create a BeautifulSoup object
        soup = BeautifulSoup(response.text, 'html.parser')

        # Open a file for writing extracted content
        with open("/Users/jeffvincent/k8s-rag-vectorizor/data/example.txt", "w", encoding="utf-8") as file:
            title = soup.title.string if soup.title else "No title"
            file.write(f"Title: {title}\n\n")
            # Iterate through all tags in the body
            for tag in soup.body.find_all(recursive=True):
                # Process paragraphs
                if tag.name == "p":
                    paragraph_text = tag.get_text().replace("\n", "")
                    if paragraph_text:
                        file.write(paragraph_text)

                # Process code blocks inside <pre><code>
                elif tag.name == "code" and tag.parent.name == "pre":
                    code_text = tag.get_text(strip=True)
                    if code_text:
                        file.write(f" ```{code_text}``` ")
