# Salas API

API para la gestión de salas y mantenimientos, construida con **FastAPI**.

## ✨ Descripción

Este repositorio contiene la base de un servicio REST para administrar:

- Salas y su estado operativo
- Mantenimientos programados
- Actividades realizadas por técnicos
- Materiales usados en mantenimiento

## 🧰 Tecnologías

- Python
- FastAPI
- Uvicorn
- MongoDB JSON Schema

## 🚀 Ejecutar el proyecto

```bash
cd app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Luego abre:

```text
http://localhost:8000
```

Documentación interactiva:

```text
http://localhost:8000/docs
```

## 📁 Estructura

```text
app/      Código principal de la API
db/       Validadores del modelo documental
docs/     Diagramas y documentación del proyecto
```

## 📌 Estado

Proyecto académico en desarrollo para el servicio de salas y mantenimiento.
