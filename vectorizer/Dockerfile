FROM python:3.11
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
COPY db.py .
COPY main.py .
CMD python main.py