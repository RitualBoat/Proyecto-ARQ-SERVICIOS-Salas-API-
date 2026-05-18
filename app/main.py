from fastapi import FastAPI, Request
import uvicorn
from models import (
    Salida,
    SalaCreate,
    SalaUpdate,
    SalasSalida,
    SalaSalida,
    MantenimientoCreate,
    MantenimientoUpdate,
    MantenimientosSalida,
    MantenimientoSalida,
)
from dao import Conexion, SalaDAO, MantenimientoDAO

app = FastAPI()


@app.get("/", tags=["Inicio"], summary="Home")
def home():
    return "Bienvenido a la servicio de Salas y su Mantenimiento"


# --- Endpoints de SALA ---
@app.post("/salas", tags=["Salas"], summary="Crear Sala", response_model=Salida)
async def crear_sala(request: Request, sala: SalaCreate) -> Salida:
    salaDAO = SalaDAO(request.app.cn.db)
    return salaDAO.crear(sala)


@app.get("/salas", tags=["Salas"], summary="Listar Salas", response_model=SalasSalida)
async def listar_salas(request: Request) -> SalasSalida:
    salaDAO = SalaDAO(request.app.cn.db)
    return salaDAO.consulta_general()


@app.get(
    "/salas/{idSala}", tags=["Salas"], summary="Listar Sala", response_model=SalaSalida
)
async def listar_sala(request: Request, idSala: str) -> SalaSalida:
    salaDAO = SalaDAO(request.app.cn.db)
    return salaDAO.consulta_por_id(idSala)


@app.get(
    "/salas/estatus/{estatus}",
    tags=["Salas"],
    summary="Listar Salas por Estatus",
    response_model=SalasSalida,
)
async def listar_salas_por_estatus(request: Request, estatus: str) -> SalasSalida:
    salaDAO = SalaDAO(request.app.cn.db)
    return salaDAO.consulta_por_estatus(estatus)


@app.put(
    "/salas/{idSala}", tags=["Salas"], summary="Modificar Sala", response_model=Salida
)
async def modificar_sala(request: Request, sala: SalaUpdate, idSala: str) -> Salida:
    salaDAO = SalaDAO(request.app.cn.db)
    return salaDAO.modificar(sala, idSala)


@app.delete(
    "/salas/{idSala}", tags=["Salas"], summary="Eliminar Sala", response_model=Salida
)
async def eliminar_sala(request: Request, idSala: str) -> Salida:
    salaDAO = SalaDAO(request.app.cn.db)
    return salaDAO.eliminar(idSala)


# --- Endpoints de MANTENIMIENTO ---
@app.post(
    "/mantenimientos",
    tags=["Mantenimientos"],
    summary="Crear Mantenimiento",
    response_model=Salida,
)
async def crear_mantenimiento(
    request: Request, mantenimiento: MantenimientoCreate
) -> Salida:
    mantenimientoDAO = MantenimientoDAO(request.app.cn.db)
    return mantenimientoDAO.asignar(mantenimiento)


@app.get(
    "/mantenimientos",
    tags=["Mantenimientos"],
    summary="Listar Mantenimientos",
    response_model=MantenimientosSalida,
)
async def listar_mantenimientos(request: Request) -> MantenimientosSalida:
    mantenimientoDAO = MantenimientoDAO(request.app.cn.db)
    return mantenimientoDAO.consulta_general()


@app.get(
    "/mantenimientos/sala/{idSala}",
    tags=["Mantenimientos"],
    summary="Listar Mantenimientos asignados a una Sala",
    response_model=MantenimientosSalida,
)
async def listar_mantenimientos_por_id_sala(
    request: Request, idSala: str
) -> MantenimientosSalida:
    mantenimientoDAO = MantenimientoDAO(request.app.cn.db)
    return mantenimientoDAO.consulta_por_id_sala(idSala)


@app.get(
    "/mantenimientos/{idMantenimiento}",
    tags=["Mantenimientos"],
    summary="Listar Mantenimiento",
    response_model=MantenimientoSalida,
)
async def listar_mantenimiento(
    request: Request, idMantenimiento: str
) -> MantenimientoSalida:
    mantenimientoDAO = MantenimientoDAO(request.app.cn.db)
    return mantenimientoDAO.consulta_por_id(idMantenimiento)


@app.get(
    "/mantenimientos/estatus/{estatus}",
    tags=["Mantenimientos"],
    summary="Listar Mantenimientos por Estatus",
    response_model=MantenimientosSalida,
)
async def listar_mantenimientos_por_estatus(
    request: Request, estatus: str
) -> MantenimientosSalida:
    mantenimientoDAO = MantenimientoDAO(request.app.cn.db)
    return mantenimientoDAO.consulta_por_estatus(estatus)


@app.put(
    "/mantenimientos/{idMantenimiento}",
    tags=["Mantenimientos"],
    summary="Modificar Mantenimiento",
    response_model=Salida,
)
async def modificar_mantenimiento(
    request: Request, mantenimiento: MantenimientoUpdate, idMantenimiento: str
) -> Salida:
    mantenimientoDAO = MantenimientoDAO(request.app.cn.db)
    return mantenimientoDAO.modificar(mantenimiento, idMantenimiento)


# --- Endpoints de ACTIVIDAD ---


# --- Endpoints de MATERIAL ---


# --- Eventos de ciclo de vida y arranque ---
@app.on_event("startup")
def startup():
    conexion = Conexion()
    app.cn = conexion


@app.on_event("shutdown")
def shutdown():
    app.cn.cerrar()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
