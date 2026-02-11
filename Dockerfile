    FROM python:3.14-slim

    WORKDIR /app

    # Copiamos requirements e instalamos
    COPY requirements.txt .
    RUN pip install -r requirements.txt

    # Copiamos el resto del código
    COPY . .

    # Exponemos el puerto donde corre FastAPI
    EXPOSE 8000

    # Arrancamos la API
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]