    # Etapa 1: La Base
    FROM python:3.9-slim

    # Etapa 2: Instalar Herramientas del Sistema (Tesseract y Poppler para PDFs)
    RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-spa poppler-utils

    # Etapa 3: Preparar el Espacio de Trabajo
    WORKDIR /app

    # Etapa 4: Instalar Dependencias de Python
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    # Etapa 5: Copiar el Código de la Aplicación
    COPY . .

    # Etapa 6: El Comando Final para Iniciar
    CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
    