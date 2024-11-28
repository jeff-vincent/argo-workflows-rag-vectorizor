import scrapy
from bs4 import BeautifulSoup
import os

def get_start_urls():
    url_files = os.listdir(os.path.join('/Users/jeffvincent/k8s-rag-vectorizor/input'))
    urls = []
    for url_file in url_files:
        with open(os.path.join('/Users/jeffvincent/k8s-rag-vectorizor/input', url_file), 'r') as file:
            urls.extend(file.readlines())

    return urls

class RagSpider(scrapy.Spider):
    name = "rag_spider"
    start_urls = get_start_urls()

    def parse(self, response):
        url = None
        output_filepath = None
        for k, v in response.__dict__.items():
            if k == '_url':
                url = v
                filename = v.split('/')[-2]
                print(filename)
                output_filepath = os.path.join(f'/Users/jeffvincent/k8s-rag-vectorizor/data/{filename}.txt')

        soup = BeautifulSoup(response.text, 'html.parser')

        with open(output_filepath, "w", encoding="utf-8") as file:
            title = soup.title.string if soup.title else "No title"
            file.write(f"Title: {title}\n\n")
            file.write(f"URL: {url}\n\n")
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
