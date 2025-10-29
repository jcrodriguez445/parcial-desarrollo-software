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

class ProyectoBase(SQLModel):
    nombre: str = Field(..., min_length=1, max_length=150)
    descripcion: Optional[str] = Field(default=None, max_length=1000)
    presupuesto: float = Field(..., gt=0)
    estado: EstadoProyecto = Field(default=EstadoProyecto.PLANIFICADO)

class Proyecto(ProyectoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    gerente_id: Optional[int] = Field(default=None, foreign_key="empleado.id")
    gerente: Optional[Empleado] = Relationship(sa_relationship_kwargs={"lazy": "select"}, back_populates=None)
    empleados: List[Empleado] = Relationship(back_populates="proyectos", link_model=VínculoProyectoEmpleado)

class ProyectoCrear(ProyectoBase):
    gerente_id: int

class ProyectoLeer(ProyectoBase):
    id: int
    gerente_id: Optional[int]

class HistorialEmpleadoEliminado(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    especialidad: str
    salario: float
    estado: str
    fecha_eliminacion: datetime = Field(default_factory=datetime.now)

class HistorialProyectoEliminado(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: Optional[str]
    presupuesto: float
    estado: str
    gerente_id: Optional[int]
    fecha_eliminacion: datetime = Field(default_factory=datetime.now