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
    ActividadCreate, 
    ActividadUpdate, 
    ActividadSalida, 
    ActividadesSalida, 
    MaterialCreate, 
    MaterialUpdate, 
    MaterialSalida, 
    MaterialesSalida
)
from dao import Conexion, SalaDAO, MantenimientoDAO, ActividadDAO, MaterialDAO

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
@app.post("/actividades", tags=["Actividades"], summary="Crear Actividad", response_model=Salida)
async def crear_actividad(request: Request, actividad: ActividadCreate) -> Salida:
    dao = ActividadDAO(request.app.cn.db)
    return dao.crear(actividad)

@app.get("/actividades", tags=["Actividades"], summary="Listar Actividades", response_model=ActividadesSalida)
async def listar_actividades(request: Request) -> ActividadesSalida:
    dao = ActividadDAO(request.app.cn.db)
    return dao.consulta_general()

@app.get("/actividades/{idActividad}", tags=["Actividades"], summary="Consultar Actividad", response_model=ActividadSalida)
async def listar_actividad(request: Request, idActividad: str) -> ActividadSalida:
    dao = ActividadDAO(request.app.cn.db)
    return dao.consulta_por_id(idActividad)

@app.put("/actividades/{idActividad}", tags=["Actividades"], summary="Modificar Actividad", response_model=Salida)
async def modificar_actividad(request: Request, actividad: ActividadUpdate, idActividad: str) -> Salida:
    dao = ActividadDAO(request.app.cn.db)
    return dao.modificar(actividad, idActividad)

@app.delete("/actividades/{idActividad}", tags=["Actividades"], summary="Eliminar Actividad", response_model=Salida)
async def eliminar_actividad(request: Request, idActividad: str) -> Salida:
    dao = ActividadDAO(request.app.cn.db)
    return dao.eliminar(idActividad)


# --- Endpoints de MATERIAL ---
@app.post("/materiales", tags=["Materiales"], summary="Crear Material", response_model=Salida)
async def crear_material(request: Request, material: MaterialCreate) -> Salida:
    dao = MaterialDAO(request.app.cn.db)
    return dao.crear(material)

@app.get("/materiales", tags=["Materiales"], summary="Listar Materiales", response_model=MaterialesSalida)
async def listar_materiales(request: Request) -> MaterialesSalida:
    dao = MaterialDAO(request.app.cn.db)
    return dao.consulta_general()

@app.get("/materiales/{idMaterial}", tags=["Materiales"], summary="Consultar Material", response_model=MaterialSalida)
async def listar_material(request: Request, idMaterial: str) -> MaterialSalida:
    dao = MaterialDAO(request.app.cn.db)
    return dao.consulta_por_id(idMaterial)

@app.put("/materiales/{idMaterial}", tags=["Materiales"], summary="Modificar Material", response_model=Salida)
async def modificar_material(request: Request, material: MaterialUpdate, idMaterial: str) -> Salida:
    dao = MaterialDAO(request.app.cn.db)
    return dao.modificar(material, idMaterial)

@app.delete("/materiales/{idMaterial}", tags=["Materiales"], summary="Eliminar Material", response_model=Salida)
async def eliminar_material(request: Request, idMaterial: str) -> Salida:
    dao = MaterialDAO(request.app.cn.db)
    return dao.eliminar(idMaterial)


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
