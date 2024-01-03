FROM python:3.11-bookworm
WORKDIR /app
COPY app .
RUN pip install -r requirements.txt
RUN python3 -m spacy download en_core_web_sm
CMD [ "python3", "app.py" ]
