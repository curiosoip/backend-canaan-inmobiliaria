# Imagen base liviana de Python
FROM python:3.13-slim

# Establecer directorio de trabajo
WORKDIR /app

# Evitar creación de archivos pyc y salida no bufferizada
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto para Railway
EXPOSE 8000

# Comando por defecto (ASGI con Uvicorn)
CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
