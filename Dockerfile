FROM python:3.11-slim

WORKDIR /app

# Copiar primero las dependencias para aprovechar la caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente (app.py)
COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]