FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Use uvicorn to run FastAPI
CMD ["uvicorn", "leads_crud.presentation.endpoints:app", "--host", "0.0.0.0", "--port", "8000"]