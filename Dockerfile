# Dockerile
FROM python:3.9

ADD main.py .

ENV LOAD_FACTOR=0.1
ENV THREAD_COUNT=6

CMD ["python", "./main.py"]