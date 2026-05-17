from pydantic import BaseModel, model_validator, Field
from datetime import datetime, timezone
from typing import List, Literal


# --- Modelos de ENTIDAD ---
class Sala(BaseModel):
    idSala: str
    nombre: str
    ubicacion: str
    capacidad: int
    estatus: Literal["DISPONIBLE", "OCUPADA", "EN_MANTENIMIENTO", "CLAUSURADA"]
    tipo: Literal["LABORATORIO", "AUDITORIO", "AULA", "OTRO"]
    idDepartamento: str


class Mantenimiento(BaseModel):
    idMantenimiento: str
    estatus: Literal["PENDIENTE", "ACTIVO", "CERRADO", "CANCELADO"]
    fechaInicio: datetime
    fechaFin: datetime
    idSala: str
    actividades: List[str]


# --- Modelos de ENTRADA ---


# Sala
class SalaCreate(BaseModel):
    nombre: str = Field(..., min_length=1)
    ubicacion: str = Field(..., min_length=1)
    capacidad: int = Field(..., gt=0)
    tipo: Literal["LABORATORIO", "AUDITORIO", "AULA", "OTRO"]


class SalaUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=1)
    ubicacion: str | None = Field(None, min_length=1)
    capacidad: int | None = Field(None, gt=0)
    tipo: Literal["LABORATORIO", "AUDITORIO", "AULA", "OTRO"] | None = None
    estatus: (
        Literal["DISPONIBLE", "OCUPADA", "EN_MANTENIMIENTO", "CLAUSURADA"] | None
    ) = None


# Mantenimiento
class MantenimientoCreate(BaseModel):
    fechaInicio: datetime
    fechaFin: datetime
    idSala: str

    @model_validator(mode="after")
    def validar_fechas(self):
        if self.fechaInicio > self.fechaFin:
            raise ValueError("La fecha de inicio debe ser menor o igual a la fecha fin")
        return self


class MantenimientoUpdate(BaseModel):
    fechaInicio: datetime | None = None
    fechaFin: datetime | None = None
    estatus: Literal["PENDIENTE", "ACTIVO", "CERRADO", "CANCELADO"] | None = None

    @model_validator(mode="after")
    def validar_fechas(self):
        if self.fechaInicio is not None and self.fechaFin is not None:
            if self.fechaInicio > self.fechaFin:
                raise ValueError(
                    "La fecha de inicio debe ser menor o igual a la fecha fin"
                )
        return self


# --- Modelos de SALIDA ---


# Default
class Salida(BaseModel):
    codigo: int
    mensaje: str


# Sala
class SalaSalida(Salida):
    sala: Sala | None = None


class SalasSalida(Salida):
    salas: List[Sala] | None = None


# Mantenimiento
class MantenimientoSalida(Salida):
    mantenimiento: Mantenimiento | None = None


class MantenimientosSalida(Salida):
    mantenimientos: List[Mantenimiento] | None = None
