import os
# from openai import OpenAI
import spacy

class Vectorize():
    def __init__(self):
        self.input_file_path = '/path/to/pv/mount'
        # self.openai_api_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.data = None
        self.chunks = []
        self.chunker = spacy.load("en_core_web_sm")
        self.source_metadata = None

    def read_data_from_storage(self):
        self.data = ["""
                     The problem was further exacerbated as we use Karpenter to optimize resource usage in our k8s cluster. So the scale-in of nodes happened very fast after a couple of Pods were completed. The behavior is to evict the remaining Pods on those nodes to re-distribute them to other nodes, thus reducing the number of total nodes and saving costs.
CeleryExecutor to the rescue
Considering all that, we decided to turn to the good old Celery Executor. By now having fixed worker nodes, it fits our use case of having many small and quick tasks perfectly. The average runtime of a DBT job decreased significantly as now we don’t have to wait before it initiates.
By using Airflow’s official latest helm chart, we can benefit from the KEDA autoscaler to increase or decrease the number of celery workers on demand, so we don’t pay extra costs for idle workers. It works by fetching the number of running and queued tasks in Airflow’s database and then scaling the number of workers accordingly, depending on your worker concurrency configuration.
For the case of custom jobs that require more resources, we have the option of running them using the KubernetesPodOperator. So we can still have runtime isolation for specific dependencies (without the need to install them in Airflow’s image), and the benefit of defining individual resource requests per task.
At the moment we are still considering the adoption of the KubernetesCeleryExecutor , as it enables jobs to be scheduled in two separate queues — the k8s and Celery one. It can be beneficial for scenarios when some jobs are more suited to Celery and other ones are more suited to Kubernetes.
Decoupling and dynamic DAG generation
The Data Engineering team is not the only one writing Airflow DAGs. To accommodate a scenario where individual teams will write their own DAGs, we needed a multi-repo approach for DAGs. But, at the same time, keep things consistent and enforce guidelines.
Supporting a multi-repo approach for DAGs
DAGs can be developed in individual repositories, owned by different teams, and still end up in the same Airflow instance. And of course, without embedding DAGs into Airflow’s image 😉
Trust me, you don’t want to restart the scheduler and workersevery time someone changes one line in a DAG.

"""]
        pass

    def vectorize_data(self):
        for item in self.data:
            self._chunk_data(item)
            for chunk in self.chunks:
                print(len(chunk))
                # response = self.openai.Embedding.create(
                #     input=chunk,
                #     model="text-embedding-ada-002")
                # embedding = response['data'][0]['embedding']



    def _chunk_data(self, data):
        max_length = 700
        doc = self.chunker(data)
        self.chunks = []
        chunk = ''
        buffer = []
        for sent in doc.sents:
            if len(sent) + 1 +len(chunk) <= max_length:
                chunk += " " + sent.text
                buffer.append(sent.text)
                if len(buffer) >= 4:
                    buffer = buffer[1:]
            else:
                self.chunks.append(chunk)
                chunk = " ".join(buffer)+ " " + sent.text
            
        

    def write_vectorized_data_to_mongodb(self):
        pass

    def clean_up(self):
        pass

def main():
    vectorizer = Vectorize()
    vectorizer.read_data_from_storage()
    vectorizer.vectorize_data()
    vectorizer.write_vectorized_data_to_mongodb()
    vectorizer.clean_up()


if __name__ == "__main__":
    main()
