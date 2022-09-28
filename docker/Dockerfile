FROM python:3.9-slim-buster

COPY . .
RUN ["pip", "install", "-r", "docker/requirements.txt"]

ARG PORT
ENV port=$PORT 
ARG HOST
ENV host=$HOST

EXPOSE ${port}
CMD uvicorn main:app --host ${host} --port ${port}
#CMD ["uvicorn", "main:app", "--host", ${host}, "--port", ${port}]