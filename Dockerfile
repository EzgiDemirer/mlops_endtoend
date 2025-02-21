# Base image olarak Python kullan
FROM python:3.10

RUN mkdir code/

WORKDIR code/

COPY . . 

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8080

CMD [ "uvicorn","main:app","--host=0.0.0.0","--port=8080"]





