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
)
from bson import ObjectId

DATABASE_URL = "mongodb://localhost:27017/"
DATABASE = "SalasMantenimiento"


class Conexion:
    _cliente = None
    _db = None

    def __init__(self):
        try:
            self._cliente = MongoClient(DATABASE_URL)
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
        return self._db


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
