FROM python:3.9-slim
RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-spa
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]