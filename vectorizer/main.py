import os
# from openai import OpenAI
import spacy
from datetime import datetime

from db import rag_collection

def get_input_files(input_dir_path):
    filnames = os.listdir(input_dir_path)
    file_paths = []
    for filename in filnames:
        file_paths.append(os.path.join(input_dir_path, filename))

    return file_paths


class Vectorize():
    def __init__(self):
        self.input_dir_path = '/mnt/data'
        self.input_files = get_input_files(self.input_dir_path)
        # self.openai_api_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.data = None
        self.chunks = []
        self.chunker = spacy.load("en_core_web_sm")
        self.source_metadata = None
        self.doc_title = None
        self.url = None

    def run(self):
        print('Iterating over input files...')
        for file in self.input_files:
            with open(file, 'r') as f:
                for line in f:
                    if "Title" in line:
                        self.doc_title = line.replace("Title: ", "").strip()
                    if "URL" in line:
                        self.url = line.replace("URL: ", "").strip()
                        break

                self.data = f.readlines()
            self._vectorize_data()

    def _vectorize_data(self):
            print('Chunking input data ...')
            self._chunk_data(self.data[1].replace("\n", ""))

            for chunk in self.chunks:
                print('********************************')
                print(chunk)
                print('********************************')
                mongodb_doc = {'chunk': chunk, 'page_title': self.doc_title, 'page_url': self.url, 'date_scraped': datetime.now()}
                # response = self.openai.Embedding.create(
                #     input=chunk,
                #     model="text-embedding-ada-002")
                # embedding = response['data'][0]['embedding']
                embedding = None
                mongodb_doc['embedding'] = embedding
                print(mongodb_doc)
                self._write_vectorized_data_to_mongodb(mongodb_doc)

    def _chunk_data(self, data):
        max_length = 100
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

    def _write_vectorized_data_to_mongodb(self, mongo_doc):
        # try:
        #     r = rag_collection.find({'page_title': mongo_doc['page_title']})
        #     # upsert
        # except:
        print('Writing to mongodb ...')
        r = rag_collection.insert_one(mongo_doc)
        print(r)

    def clean_up(self):
        for file in self.input_files:
            os.remove(file)


def main():
    vectorizer = Vectorize()
    print('Starting vectorizer...')
    vectorizer.run()
    # vectorizer.clean_up()


if __name__ == "__main__":
    main()
