# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.10.10
# FROM python:${PYTHON_VERSION}-slim as base
# Usa una imagen base de Python
FROM python:3.10.10-slim-buster

# Establece la variable de entorno PYTHONDONTWRITEBYTECODE para evitar que python escriba archivos pyc.
ENV PYTHONDONTWRITEBYTECODE=1

# Establece la variable de entorno PYTHONUNBUFFERED para evitar que Python haga buffering de la salida
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo en /app
WORKDIR /app

# Crea un usuario sin privilegios bajo el que se ejecutará la aplicación.
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Descarga las dependencias del proyecto
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

USER appuser

# Copia el codigo fuente al contenedor
COPY . .

# Puerto de la app
EXPOSE 8000

# Ejecuta la app
CMD python manage.py runserver
