from fastapi import Depends, FastAPI, Request
import uvicorn
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
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
    MaterialesSalida,
    Usuario,
)
from dao import Conexion, SalaDAO, MantenimientoDAO, ActividadDAO, MaterialDAO
from security import RoleChecker

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

allow_admin = RoleChecker(["Administrador"])
allow_admin_tecnico = RoleChecker(["Administrador", "Tecnico"])
allow_admin_organizador = RoleChecker(["Administrador", "Organizador"])
allow_all_roles = RoleChecker(["Administrador", "Tecnico", "Organizador"])


@app.get("/", tags=["Inicio"], summary="Home")
def home():
    return "Bienvenido a la servicio de Salas y su Mantenimiento"


# --- Endpoints de SALA ---
@app.post("/salas", tags=["Salas"], summary="Crear Sala", response_model=Salida)
@limiter.limit("5/minute")
async def crear_sala(
    request: Request,
    sala: SalaCreate,
    user: Usuario = Depends(allow_admin),
) -> Salida:
    cn = Conexion(user.username, user.password)
    try:
        salaDAO = SalaDAO(cn.db)
        salida = salaDAO.crear(sala)
    finally:
        cn.cerrar()
    return salida


@app.get("/salas", tags=["Salas"], summary="Listar Salas", response_model=SalasSalida)
@limiter.limit("5/minute")
async def listar_salas(
    request: Request,
    user: Usuario = Depends(allow_all_roles),
) -> SalasSalida:
    cn = Conexion(user.username, user.password)
    try:
        salaDAO = SalaDAO(cn.db)
        salida = salaDAO.consulta_general()
    finally:
        cn.cerrar()
    return salida


@app.get(
    "/salas/{idSala}", tags=["Salas"], summary="Listar Sala", response_model=SalaSalida
)
@limiter.limit("5/minute")
async def listar_sala(
    request: Request,
    idSala: str,
    user: Usuario = Depends(allow_all_roles),
) -> SalaSalida:
    cn = Conexion(user.username, user.password)
    try:
        salaDAO = SalaDAO(cn.db)
        salida = salaDAO.consulta_por_id(idSala)
    finally:
        cn.cerrar()
    return salida


@app.get(
    "/salas/estatus/{estatus}",
    tags=["Salas"],
    summary="Listar Salas por Estatus",
    response_model=SalasSalida,
)
@limiter.limit("5/minute")
async def listar_salas_por_estatus(
    request: Request,
    estatus: str,
    user: Usuario = Depends(allow_all_roles),
) -> SalasSalida:
    cn = Conexion(user.username, user.password)
    try:
        salaDAO = SalaDAO(cn.db)
        salida = salaDAO.consulta_por_estatus(estatus)
    finally:
        cn.cerrar()
    return salida


@app.put(
    "/salas/{idSala}", tags=["Salas"], summary="Modificar Sala", response_model=Salida
)
@limiter.limit("5/minute")
async def modificar_sala(
    request: Request,
    sala: SalaUpdate,
    idSala: str,
    user: Usuario = Depends(allow_admin_organizador),
) -> Salida:
    cn = Conexion(user.username, user.password)
    try:
        salaDAO = SalaDAO(cn.db)
        salida = salaDAO.modificar(sala, idSala)
    finally:
        cn.cerrar()
    return salida


@app.delete(
    "/salas/{idSala}", tags=["Salas"], summary="Eliminar Sala", response_model=Salida
)
@limiter.limit("5/minute")
async def eliminar_sala(
    request: Request,
    idSala: str,
    user: Usuario = Depends(allow_admin),
) -> Salida:
    cn = Conexion(user.username, user.password)
    try:
        salaDAO = SalaDAO(cn.db)
        salida = salaDAO.eliminar(idSala)
    finally:
        cn.cerrar()
    return salida


# --- Endpoints de MANTENIMIENTO ---
@app.post(
    "/mantenimientos",
    tags=["Mantenimientos"],
    summary="Crear Mantenimiento",
    response_model=Salida,
)
@limiter.limit("5/minute")
async def crear_mantenimiento(
    request: Request,
    mantenimiento: MantenimientoCreate,
    user: Usuario = Depends(allow_admin_organizador),
) -> Salida:
    cn = Conexion(user.username, user.password)
    try:
        mantenimientoDAO = MantenimientoDAO(cn.db)
        salida = mantenimientoDAO.asignar(mantenimiento)
    finally:
        cn.cerrar()
    return salida


@app.get(
    "/mantenimientos",
    tags=["Mantenimientos"],
    summary="Listar Mantenimientos",
    response_model=MantenimientosSalida,
)
@limiter.limit("5/minute")
async def listar_mantenimientos(
    request: Request,
    user: Usuario = Depends(allow_all_roles),
) -> MantenimientosSalida:
    cn = Conexion(user.username, user.password)
    try:
        mantenimientoDAO = MantenimientoDAO(cn.db)
        salida = mantenimientoDAO.consulta_general()
    finally:
        cn.cerrar()
    return salida


@app.get(
    "/mantenimientos/sala/{idSala}",
    tags=["Mantenimientos"],
    summary="Listar Mantenimientos asignados a una Sala",
    response_model=MantenimientosSalida,
)
@limiter.limit("5/minute")
async def listar_mantenimientos_por_id_sala(
    request: Request,
    idSala: str,
    user: Usuario = Depends(allow_all_roles),
) -> MantenimientosSalida:
    cn = Conexion(user.username, user.password)
    try:
        mantenimientoDAO = MantenimientoDAO(cn.db)
        salida = mantenimientoDAO.consulta_por_id_sala(idSala)
    finally:
        cn.cerrar()
    return salida


@app.get(
    "/mantenimientos/{idMantenimiento}",
    tags=["Mantenimientos"],
    summary="Listar Mantenimiento",
    response_model=MantenimientoSalida,
)
@limiter.limit("5/minute")
async def listar_mantenimiento(
    request: Request,
    idMantenimiento: str,
    user: Usuario = Depends(allow_all_roles),
) -> MantenimientoSalida:
    cn = Conexion(user.username, user.password)
    try:
        mantenimientoDAO = MantenimientoDAO(cn.db)
        salida = mantenimientoDAO.consulta_por_id(idMantenimiento)
    finally:
        cn.cerrar()
    return salida


@app.get(
    "/mantenimientos/estatus/{estatus}",
    tags=["Mantenimientos"],
    summary="Listar Mantenimientos por Estatus",
    response_model=MantenimientosSalida,
)
@limiter.limit("5/minute")
async def listar_mantenimientos_por_estatus(
    request: Request,
    estatus: str,
    user: Usuario = Depends(allow_all_roles),
) -> MantenimientosSalida:
    cn = Conexion(user.username, user.password)
    try:
        mantenimientoDAO = MantenimientoDAO(cn.db)
        salida = mantenimientoDAO.consulta_por_estatus(estatus)
    finally:
        cn.cerrar()
    return salida


@app.put(
    "/mantenimientos/{idMantenimiento}",
    tags=["Mantenimientos"],
    summary="Modificar Mantenimiento",
    response_model=Salida,
)
@limiter.limit("5/minute")
async def modificar_mantenimiento(
    request: Request,
    mantenimiento: MantenimientoUpdate,
    idMantenimiento: str,
    user: Usuario = Depends(allow_admin_organizador),
) -> Salida:
    cn = Conexion(user.username, user.password)
    try:
        mantenimientoDAO = MantenimientoDAO(cn.db)
        salida = mantenimientoDAO.modificar(mantenimiento, idMantenimiento)
    finally:
        cn.cerrar()
    return salida


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
    conexion = Conexion("", "")
    app.cn = conexion


@app.on_event("shutdown")
def shutdown():
    app.cn.cerrar()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
