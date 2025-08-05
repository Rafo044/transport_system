FROM python:3.10-slim

WORKDIR /app
COPY etl.py .

RUN pip install memphis-py psycopg2-binary

CMD ["python", "etl.py"]
