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
        return salida

    def consulta_general(self):
        salida = SalasSalida(codigo=0, mensaje="", salas=[])
        return salida

    def consulta_por_id(self, idSala: str):
        salida = SalaSalida(codigo=0, mensaje="", sala=None)
        return salida

    def consulta_por_estatus(self, estatus):
        salida = SalasSalida(codigo=0, mensaje="", salas=[])
        return salida

    def modificar(self, sala: SalaUpdate, idSala: str):
        salida = Salida(codigo=0, mensaje="")
        return salida

    def eliminar(self, idSala: str):
        salida = Salida(codigo=0, mensaje="")
        return salida


class MantenimientoDAO:
    def __init__(self, db):
        return

    def asignar(self, mantenimiento: MantenimientoCreate):
        salida = Salida(codigo=0, mensaje="")
        return salida

    def consulta_general(self):
        salida = MantenimientosSalida(codigo=0, mensaje="", Mantenimientos=[])
        return salida

    def consulta_por_id_sala(self, idSala: str):
        salida = MantenimientosSalida(codigo=0, mensaje="", Mantenimientos=[])
        return salida

    def consulta_por_id(self, idMantenimiento: str):
        salida = MantenimientoSalida(codigo=0, mensaje="", mantenimiento=None)
        return salida

    def consulta_por_estatus(self, estatus):
        salida = MantenimientosSalida(codigo=0, mensaje="", Mantenimientos=[])
        return salida

    def modificar(self, mantenimiento: MantenimientoUpdate, idMantenimiento: str):
        salida = Salida(codigo=0, mensaje="")
        return salida
