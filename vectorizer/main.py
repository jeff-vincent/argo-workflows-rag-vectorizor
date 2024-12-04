import os
import secrets
from openai import OpenAI
import spacy
from pymongo import DeleteMany, InsertOne
from datetime import datetime
from bson import ObjectId

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
        self.openai_api_client = OpenAI(api_key='')
        self.data = None
        self.chunks = []
        self.chunker = spacy.load("en_core_web_sm")
        self.source_metadata = None
        self.doc_title = None
        self.url = None
        self.mongodb_docs = None

    def run(self):
        print('Iterating over input files...')
        for file in self.input_files:
            self.mongodb_docs = []
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
                mongodb_doc = {'chunk': chunk, 'page_title': self.doc_title, 'page_url': self.url, 'date_scraped': datetime.now()}
                response = self.openai_api_client.embeddings.create(
                    input=chunk,
                    model="text-embedding-ada-002")
                embedding = response.data[0].embedding
                # embedding = None
                mongodb_doc['embedding'] = embedding
                self.mongodb_docs.append(mongodb_doc)
                self._write_vectorized_data_to_mongodb()

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

    def _write_vectorized_data_to_mongodb(self):
        print('Writing to mongodb ...')
        url = self.mongodb_docs[0]['page_url']
        bulk_operations_list = [DeleteMany({'page_url': url})]
        for mongo_doc in self.mongodb_docs:
            random_string = secrets.token_hex(12)
            mongo_doc['_id'] = ObjectId(random_string)
            bulk_operations_list.append(InsertOne(mongo_doc))
        r = rag_collection.bulk_write(bulk_operations_list)
        print(r)

    def clean_up(self):
        for file in self.input_files:
            os.remove(file)


def main():
    vectorizer = Vectorize()
    print('Starting vectorizer...')
    vectorizer.run()
    vectorizer.clean_up()


if __name__ == "__main__":
    main()
