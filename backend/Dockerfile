# syntax=docker/dockerfile:1
FROM python:3.10.10
WORKDIR /backend
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# Download the medium-sized English model
RUN python -m spacy download en_core_web_md
EXPOSE 3001
COPY . .
CMD ["python", "app.py"]