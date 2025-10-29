from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from datetime import datetime

class EstadoEmpleado(str, Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"

class EstadoProyecto(str, Enum):
    PLANIFICADO = "planificado"
    EN_PROGRESO = "en_progreso"
    COMPLETADO = "completado"
    CANCELADO = "cancelado"

class VínculoProyectoEmpleado(SQLModel, table=True):
    proyecto_id: Optional[int] = Field(default=None, foreign_key="proyecto.id", primary_key=True)
    empleado_id: Optional[int] = Field(default=None, foreign_key="empleado.id", primary_key=True)
    rol: Optional[str] = Field(default=None, max_length=100)

class EmpleadoBase(SQLModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    especialidad: str = Field(..., min_length=1, max_length=100)
    salario: float = Field(..., gt=0)
    estado: EstadoEmpleado = Field(default=EstadoEmpleado.ACTIVO)

class Empleado(EmpleadoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    proyectos: List["Proyecto"] = Relationship(back_populates="empleados", link_model=VínculoProyectoEmpleado)

class EmpleadoCrear(EmpleadoBase):
    pass

class EmpleadoLeer(EmpleadoBase):
    id: int