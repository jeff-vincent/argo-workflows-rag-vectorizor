import os
# from openai import OpenAI
import spacy
import time

class Vectorize():
    def __init__(self):
        self.input_file_path = '/Users/jeffvincent/k8s-rag-vectorizor/data/example.txt'
        # self.openai_api_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.data = None
        self.chunks = []
        self.chunker = spacy.load("en_core_web_sm")
        self.source_metadata = None
        self.doc_title = None

    def read_data_from_storage(self):
        with open(self.input_file_path, 'r') as f:
            for line in f:
                if "Title" in line:
                    self.doc_title = line.strip()
                    continue

            self.data = f.readlines()

    def vectorize_data(self):
        for item in self.data:
            self._chunk_data(item)
            for chunk in self.chunks:
                mongodb_doc = {'chunk': chunk, 'page_title': item, 'page_url': item, 'date_scraped': time.now()}
                # response = self.openai.Embedding.create(
                #     input=chunk,
                #     model="text-embedding-ada-002")
                # embedding = response['data'][0]['embedding']
                embedding = None
                mongodb_doc['embedding'] = embedding
                self.write_vectorized_data_to_mongodb(mongodb_doc)

    def _chunk_data(self, data):
        max_length = 4000
        doc = self.chunker(data)
        self.chunks = []
        chunk = ''
        buffer = []
        for sent in doc.sents:
            if len(sent) + 1 +len(chunk) <= max_length:
                chunk += " " + sent.text
                buffer.append(sent.text)
                if len(buffer) >= 3:
                    buffer = buffer[1:]
            else:
                self.chunks.append(chunk)
                chunk = " ".join(buffer)+ " " + sent.text

    def write_vectorized_data_to_mongodb(self, data):
        print('writing vector data to mongodb')
        pass

    def clean_up(self):
        os.remove(self.input_file_path)

def main():
    vectorizer = Vectorize()
    vectorizer.read_data_from_storage()
    vectorizer.vectorize_data()
    # vectorizer.clean_up()


if __name__ == "__main__":
    main()
