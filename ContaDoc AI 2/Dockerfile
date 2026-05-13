# Dockerfile for Backend
FROM python:3.10-slim

# Install system dependencies for OCR (Tesseract and Poppler for pdf2image)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-por \
    poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/requirements.txt .
COPY backend/requirements_extra.txt ./requirements_extra.txt
RUN pip install --no-cache-dir -r requirements.txt -r requirements_extra.txt

COPY backend/ .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
