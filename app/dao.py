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


class SalaDAO:
    def __init__(self, db):
        return

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
