FROM python:3.12-slim
 
WORKDIR /app
 
# Install deps first (Docker layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy app code
COPY app/ .
 
EXPOSE 8000
 
# uvicorn is the ASGI server that runs FastAPI
# --workers 2 = two worker processes
# --host 0.0.0.0 = listen on all interfaces (required in containers)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
