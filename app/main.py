from fastapi import FastAPI

app = FastAPI()

@app.get("/", tags=["Inicio"], summary="Home")
def home():
    return "Bienvenido a la servicio de Salas y su Mantenimiento"

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)