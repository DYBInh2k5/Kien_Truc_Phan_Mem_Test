FROM python:3.10-slim

WORKDIR /app

COPY service3_gateway/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY service3_gateway/ .

EXPOSE 8000

CMD ["python", "main.py"]
