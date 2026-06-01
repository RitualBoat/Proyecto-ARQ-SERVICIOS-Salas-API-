from pymongo import MongoClient
from models import (
    Salida,
    SalaCreate,
    SalaUpdate,
    SalaSalida,
    SalasSalida,
    MantenimientoCreate,
    MantenimientoUpdate,
    MantenimientoSalida,
    MantenimientosSalida,
    MaterialCreate,
    MaterialUpdate,
    MaterialSalida,
    MaterialesSalida,
    ActividadCreate,
    ActividadUpdate,
    ActividadSalida,
    ActividadesSalida,
    Usuario,
)
from bson import ObjectId

DATABASE = "salas_mantenimiento"


class Conexion:
    _cliente = None
    _db = None

    def __init__(self, user, password):
        try:
            if user and password:
                self.DATABASEURL = (
                    f"mongodb://{user}:{password}@localhost:27017/?authSource=admin"
                )

            else:
                self.DATABASEURL = "mongodb://localhost:27017/"
            self._cliente = MongoClient(self.DATABASEURL)
            self._db = self._cliente[DATABASE]
            print(f"Conectado con la BD: {DATABASE}")
        except Exception as ex:
            print(f"Error al conectar con la BD a causa de: {ex}")

    def cerrar(self):
        try:
            self._cliente.close()
            print(f"Conexion cerrada con la BD:{DATABASE}")
        except Exception as ex:
            print(f"Error al cerrar con la BD a causa de: {ex}")

    @property
    def db(self):
        try:
            return self._db
        except Exception as ex:
            print("Error al obtener la conexion")


class UsuarioDAO:
    def __init__(self, db):
        self.db = db
        self.col = self.db.usuarios

    def autenticar(self, username: str, password: str):
        result = self.col.find_one(
            {"username": username, "password": password, "estatus": "ACTIVO"}
        )
        if result:
            result.pop("_id", None)
            return Usuario(**result)
        return None


class SalaDAO:
    def __init__(self, db):
        self.db = db
        self.col = self.db.salas
        self.view = self.db.salasView

    def crear(self, sala: SalaCreate):
        salida = Salida(codigo=0, mensaje="")
        try:
            data = sala.model_dump()
            data["estatus"] = "DISPONIBLE"
            data["idDepartamento"] = None
            result = self.col.insert_one(data)
            salida.codigo = 201
            salida.mensaje = "Sala creada exitosamente con id: " + str(
                result.inserted_id
            )
        except Exception as ex:
            salida.codigo = 500
            salida.mensaje = f"Error: {ex}"
        return salida

    def consulta_general(self):
        salida = SalasSalida(codigo=0, mensaje="", salas=[])
        try:
            salida.codigo = 200
            salida.mensaje = "Listado de salas"
            salida.salas = list(self.view.find().sort("nombre", 1))
        except Exception as ex:
            salida.codigo = 500
            salida.mensaje = f"Error al consultar las salas: {ex}"
            salida.salas = None
        return salida

    def consulta_por_id(self, idSala: str):
        salida = SalaSalida(codigo=0, mensaje="", sala=None)
        try:
            if not ObjectId.is_valid(idSala):
                salida.codigo = 400
                salida.mensaje = "El formato del ID no es válido."
                return salida

            res = self.view.find_one({"idSala": idSala})
            if not res:
                salida.codigo = 404
                salida.mensaje = "La sala no existe."
            else:
                salida.codigo = 200
                salida.mensaje = "Listado de la sala"
                salida.sala = res
        except Exception as ex:
            salida.codigo = 400
            salida.mensaje = f"Error:{ex}"
        return salida

    def consulta_por_estatus(self, estatus):
        salida = SalasSalida(codigo=0, mensaje="", salas=[])
        estatus_permitidos = ["DISPONIBLE", "OCUPADA", "EN_MANTENIMIENTO", "CLAUSURADA"]
        if estatus not in estatus_permitidos:
            salida.codigo = 400
            salida.mensaje = f"El estatus '{estatus}' no es un valor permitido."
            salida.salas = None
            return salida
        try:
            salida.codigo = 200
            salida.mensaje = "Listado de salas por estatus"
            salida.salas = list(self.view.find({"estatus": estatus}))
        except Exception as ex:
            salida.codigo = 400
            salida.mensaje = f"Error:{ex}"
            salida.salas = None
        return salida

    def modificar(self, sala: SalaUpdate, idSala: str):
        salida = Salida(codigo=0, mensaje="")
        if not ObjectId.is_valid(idSala):
            salida.codigo = 400
            salida.mensaje = "El formato del ID no es válido."
            return salida
        try:
            data = sala.model_dump(exclude_unset=True)
            if not data:
                salida.codigo = 400
                salida.mensaje = "Debes proporcionar al menos un campo para modificar."
                return salida

            result = self.col.update_one({"_id": ObjectId(idSala)}, {"$set": data})

            if result.matched_count == 0:
                salida.codigo = 404
                salida.mensaje = f"La sala con id: {idSala} no existe."
            elif result.modified_count == 0:
                salida.codigo = 200
                salida.mensaje = "La sala existe, pero no hubo cambios que aplicar."
            else:
                salida.codigo = 200
                salida.mensaje = f"La sala con id: {idSala} se modifico con exito."
        except Exception as ex:
            salida.codigo = 400
            salida.mensaje = f"Error al modificar la sala: {ex}"
        return salida

    def eliminar(self, idSala: str):
        salida = Salida(codigo=0, mensaje="")
        if not ObjectId.is_valid(idSala):
            salida.codigo = 400
            salida.mensaje = "El formato del ID no es válido."
            return salida
        try:
            sala_existente = self.col.find_one({"_id": ObjectId(idSala)})
            if not sala_existente:
                salida.codigo = 404
                salida.mensaje = f"La sala con id: {idSala} no existe."
                return salida

            if sala_existente.get("estatus") != "CLAUSURADA":
                salida.codigo = 400
                salida.mensaje = (
                    "No se permite eliminar la sala porque no está CLAUSURADA."
                )
                return salida

            self.col.delete_one({"_id": ObjectId(idSala)})
            salida.codigo = 200
            salida.mensaje = f"La sala con id: {idSala} se elimino con exito."
        except Exception as ex:
            salida.codigo = 400
            salida.mensaje = f"Error al eliminar la sala: {ex}"
        return salida


class MantenimientoDAO:
    def __init__(self, db):
        self.db = db
        self.col = self.db.mantenimientos
        self.view = self.db.mantenimientosView
        self.col_salas = self.db.salas

    def asignar(self, mantenimiento: MantenimientoCreate):
        salida = Salida(codigo=0, mensaje="")
        if not ObjectId.is_valid(mantenimiento.idSala):
            salida.codigo = 400
            salida.mensaje = "El idSala proporcionado no es un ObjectId válido."
            return salida
        try:
            sala_asociada = self.col_salas.find_one(
                {"_id": ObjectId(mantenimiento.idSala)}
            )
            if not sala_asociada:
                salida.codigo = 404
                salida.mensaje = "La sala informada no existe."
                return salida

            if sala_asociada.get("estatus") == "CLAUSURADA":
                salida.codigo = 400
                salida.mensaje = (
                    "No se permite asignar mantenimiento a una sala CLAUSURADA."
                )
                return salida

            data = mantenimiento.model_dump()
            data["idSala"] = ObjectId(data["idSala"])
            data["estatus"] = "PENDIENTE"
            data["actividades"] = []
            result = self.col.insert_one(data)
            salida.codigo = 201
            salida.mensaje = "Mantenimiento creado exitosamente con id: " + str(
                result.inserted_id
            )
        except Exception as ex:
            salida.codigo = 500
            salida.mensaje = f"Error al crear el mantenimiento: {ex}"
        return salida

    def consulta_general(self):
        salida = MantenimientosSalida(codigo=0, mensaje="", mantenimientos=[])
        try:
            salida.codigo = 200
            salida.mensaje = "Listado de mantenimientos"
            salida.mantenimientos = list(self.view.find().sort("fechaInicio", -1))
        except Exception as ex:
            salida.codigo = 500
            salida.mensaje = f"Error al consultar los mantenimientos: {ex}"
            salida.mantenimientos = None
        return salida

    def consulta_por_id_sala(self, idSala: str):
        salida = MantenimientosSalida(codigo=0, mensaje="", mantenimientos=[])
        try:
            if not ObjectId.is_valid(idSala):
                salida.codigo = 400
                salida.mensaje = "El formato del ID de sala no es válido."
                salida.mantenimientos = None
                return salida

            sala_existe = self.col_salas.find_one({"_id": ObjectId(idSala)})
            if not sala_existe:
                salida.codigo = 404
                salida.mensaje = "La sala informada no existe."
                salida.mantenimientos = None
                return salida

            salida.codigo = 200
            salida.mensaje = "Listado de mantenimientos por sala"
            salida.mantenimientos = list(self.view.find({"idSala": idSala}))
        except Exception as ex:
            salida.codigo = 400
            salida.mensaje = f"Error al consultar los mantenimientos: {ex}"
            salida.mantenimientos = None
        return salida

    def consulta_por_id(self, idMantenimiento: str):
        salida = MantenimientoSalida(codigo=0, mensaje="", mantenimiento=None)
        try:
            if not ObjectId.is_valid(idMantenimiento):
                salida.codigo = 400
                salida.mensaje = "El formato del ID de mantenimiento no es válido."
                return salida

            res = self.view.find_one({"idMantenimiento": idMantenimiento})
            if not res:
                salida.codigo = 404
                salida.mensaje = "El mantenimiento no existe."
            else:
                salida.codigo = 200
                salida.mensaje = "Listado del mantenimiento"
                salida.mantenimiento = res
        except Exception as ex:
            salida.codigo = 400
            salida.mensaje = f"Error al consultar el mantenimiento: {ex}"
        return salida

    def consulta_por_estatus(self, estatus):
        salida = MantenimientosSalida(codigo=0, mensaje="", mantenimientos=[])
        estatus_permitidos = ["PENDIENTE", "ACTIVO", "CERRADO", "CANCELADO"]
        if estatus not in estatus_permitidos:
            salida.codigo = 400
            salida.mensaje = (
                f"El estatus '{estatus}' no pertenece al catálogo permitido."
            )
            salida.mantenimientos = None
            return salida
        try:
            salida.codigo = 200
            salida.mensaje = "Listado de mantenimientos por estatus"
            salida.mantenimientos = list(self.view.find({"estatus": estatus}))
        except Exception as ex:
            salida.codigo = 400
            salida.mensaje = f"Error al consultar los mantenimientos: {ex}"
            salida.mantenimientos = None
        return salida

    def modificar(self, mantenimiento: MantenimientoUpdate, idMantenimiento: str):
        salida = Salida(codigo=0, mensaje="")
        if not ObjectId.is_valid(idMantenimiento):
            salida.codigo = 400
            salida.mensaje = "El formato del ID no es válido."
            return salida
        try:
            mantenimiento_previo = self.col.find_one({"_id": ObjectId(idMantenimiento)})
            if not mantenimiento_previo:
                salida.codigo = 404
                salida.mensaje = (
                    f"El mantenimiento con id: {idMantenimiento} no existe."
                )
                return salida

            data = mantenimiento.model_dump(exclude_unset=True)
            if not data:
                salida.codigo = 400
                salida.mensaje = "Debes proporcionar al menos un campo para modificar."
                return salida

            nuevo_estatus = data.get("estatus")
            if nuevo_estatus in ["CERRADO", "CANCELADO"]:
                sala_id = mantenimiento_previo.get("idSala")
                if sala_id:
                    self.col_salas.update_one(
                        {"_id": sala_id}, {"$set": {"estatus": "DISPONIBLE"}}
                    )

            result = self.col.update_one(
                {"_id": ObjectId(idMantenimiento)}, {"$set": data}
            )

            if result.modified_count == 0 and result.matched_count > 0:
                salida.codigo = 200
                salida.mensaje = (
                    "El mantenimiento existe, pero no hubo cambios que aplicar."
                )
            else:
                salida.codigo = 200
                salida.mensaje = (
                    f"El mantenimiento con id: {idMantenimiento} se modifico con exito."
                )
        except Exception as ex:
            salida.codigo = 400
            salida.mensaje = f"Error al modificar el mantenimiento: {ex}"
        return salida


# --- Entidades Actividad y Material ---
class ActividadDAO:
    def __init__(self, db):
        self.db = db
        self.col = self.db.actividades
        self.view = self.db.actividadesView

    def crear(self, actividad: ActividadCreate):
        salida = Salida(codigo=0, mensaje="")
        if not ObjectId.is_valid(actividad.idTecnico):
            salida.codigo = 400
            salida.mensaje = "El idTecnico no es válido."
            return salida

        try:
            data = actividad.model_dump()
            data["idTecnico"] = ObjectId(data["idTecnico"])
            data["completado"] = False
            data["observaciones"] = []
            data["materiales"] = []

            result = self.col.insert_one(data)
            salida.codigo = 201
            salida.mensaje = (
                f"Actividad creada exitosamente con id: {result.inserted_id}"
            )
        except Exception as ex:
            salida.codigo = 500
            salida.mensaje = f"Error al crear actividad: {ex}"
        return salida

    def consulta_general(self):
        salida = ActividadesSalida(codigo=0, mensaje="", actividades=[])
        try:
            salida.codigo = 200
            salida.mensaje = "Listado de actividades"
            salida.actividades = list(self.view.find().sort("_id", -1))
        except Exception as ex:
            salida.codigo = 500
            salida.mensaje = f"Error: {ex}"
        return salida

    def consulta_por_id(self, idActividad: str):
        salida = ActividadSalida(codigo=0, mensaje="", actividad=None)
        if not ObjectId.is_valid(idActividad):
            salida.codigo = 400
            salida.mensaje = "Formato de ID inválido."
            return salida

        try:
            res = self.view.find_one({"idActividad": idActividad})
            if res:
                salida.codigo = 200
                salida.mensaje = "Detalle de la actividad"
                salida.actividad = res
            else:
                salida.codigo = 404
                salida.mensaje = "La actividad no existe."
        except Exception as ex:
            salida.codigo = 500
            salida.mensaje = f"Error: {ex}"
        return salida

    def modificar(self, actividad: ActividadUpdate, idActividad: str):
        salida = Salida(codigo=0, mensaje="")
        if not ObjectId.is_valid(idActividad):
            salida.codigo = 400
            salida.mensaje = "Formato de ID inválido."
            return salida

        try:
            data = actividad.model_dump(exclude_unset=True)
            if not data:
                salida.codigo = 400
                salida.mensaje = "Proporcione datos para actualizar."
                return salida

            result = self.col.update_one({"_id": ObjectId(idActividad)}, {"$set": data})
            if result.matched_count == 0:
                salida.codigo = 404
                salida.mensaje = "La actividad no existe."
            else:
                salida.codigo = 200
                salida.mensaje = "Actividad modificada con éxito."
        except Exception as ex:
            salida.codigo = 500
            salida.mensaje = f"Error: {ex}"
        return salida

    def eliminar(self, idActividad: str):
        salida = Salida(codigo=0, mensaje="")
        if not ObjectId.is_valid(idActividad):
            salida.codigo = 400
            salida.mensaje = "Formato de ID inválido."
            return salida

        try:
            actividad = self.col.find_one({"_id": ObjectId(idActividad)})
            if not actividad:
                salida.codigo = 404
                salida.mensaje = "La actividad no existe."
                return salida

            if actividad.get("completado") is True:
                salida.codigo = 400
                salida.mensaje = "No se puede eliminar una actividad ya completada."
                return salida

            self.col.delete_one({"_id": ObjectId(idActividad)})
            salida.codigo = 200
            salida.mensaje = "Actividad eliminada con éxito."
        except Exception as ex:
            salida.codigo = 500
            salida.mensaje = f"Error: {ex}"
        return salida


class MaterialDAO:
    def __init__(self, db):
        self.db = db
        self.col = self.db.materiales
        self.view = self.db.materialesView
        self.col_actividades = self.db.actividades

    def crear(self, material: MaterialCreate):
        salida = Salida(codigo=0, mensaje="")
        try:
            data = material.model_dump()
            result = self.col.insert_one(data)
            salida.codigo = 201
            salida.mensaje = (
                f"Material creado exitosamente con id: {result.inserted_id}"
            )
        except Exception as ex:
            salida.codigo = 500
            salida.mensaje = f"Error: {ex}"
        return salida

    def consulta_general(self):
        salida = MaterialesSalida(codigo=0, mensaje="", materiales=[])
        try:
            salida.codigo = 200
            salida.mensaje = "Listado de materiales"
            salida.materiales = list(self.view.find().sort("nombre", 1))
        except Exception as ex:
            salida.codigo = 500
            salida.mensaje = f"Error: {ex}"
        return salida

    def consulta_por_id(self, idMaterial: str):
        salida = MaterialSalida(codigo=0, mensaje="", material=None)
        if not ObjectId.is_valid(idMaterial):
            salida.codigo = 400
            salida.mensaje = "Formato de ID inválido."
            return salida
        try:
            res = self.view.find_one({"idMaterial": idMaterial})
            if res:
                salida.codigo = 200
                salida.mensaje = "Detalle del material"
                salida.material = res
            else:
                salida.codigo = 404
                salida.mensaje = "El material no existe."
        except Exception as ex:
            salida.codigo = 500
            salida.mensaje = f"Error: {ex}"
        return salida

    def modificar(self, material: MaterialUpdate, idMaterial: str):
        salida = Salida(codigo=0, mensaje="")
        if not ObjectId.is_valid(idMaterial):
            salida.codigo = 400
            salida.mensaje = "Formato de ID inválido."
            return salida
        try:
            data = material.model_dump(exclude_unset=True)
            if not data:
                salida.codigo = 400
                salida.mensaje = "Proporcione datos para modificar."
                return salida

            result = self.col.update_one({"_id": ObjectId(idMaterial)}, {"$set": data})
            if result.matched_count == 0:
                salida.codigo = 404
                salida.mensaje = "El material no existe."
            else:
                salida.codigo = 200
                salida.mensaje = "Material modificado con éxito."
        except Exception as ex:
            salida.codigo = 500
            salida.mensaje = f"Error: {ex}"
        return salida

    def eliminar(self, idMaterial: str):
        salida = Salida(codigo=0, mensaje="")
        if not ObjectId.is_valid(idMaterial):
            salida.codigo = 400
            salida.mensaje = "Formato de ID inválido."
            return salida
        try:
            en_uso = self.col_actividades.find_one(
                {"materiales.idMaterial": ObjectId(idMaterial), "completado": False}
            )
            if en_uso:
                salida.codigo = 400
                salida.mensaje = "El material no puede eliminarse, está asignado a una actividad activa."
                return salida

            result = self.col.delete_one({"_id": ObjectId(idMaterial)})
            if result.deleted_count > 0:
                salida.codigo = 200
                salida.mensaje = "Material eliminado con éxito."
            else:
                salida.codigo = 404
                salida.mensaje = "El material no existe."
        except Exception as ex:
            salida.codigo = 500
            salida.mensaje = f"Error: {ex}"
        return salida
