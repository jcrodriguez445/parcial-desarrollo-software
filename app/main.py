from fastapi import FastAPI, Depends, Query
from typing import List
from sqlmodel import Session, select
from app.database import inicializar_bd, obtener_sesion
from app.modelos import Empleado, EmpleadoCrear, EmpleadoLeer, Proyecto, ProyectoCrear, ProyectoLeer, EstadoEmpleado, EstadoProyecto, HistorialEmpleadoEliminado, HistorialProyectoEliminado
import app.crud as crud

app = FastAPI(title="Sistema de Gestión de Proyectos - Parcial", version="1.0")

@app.on_event("startup")
def startup():
    inicializar_bd()

# ----- EMPLEADOS -----

@app.post("/empleados", response_model=EmpleadoLeer, status_code=201)
def crear_empleado_endpoint(empleado: EmpleadoCrear, sesion: Session = Depends(obtener_sesion)):
    nuevo = Empleado.from_orm(empleado)
    return crud.crear_empleado(sesion, nuevo)

@app.get("/empleados", response_model=List[EmpleadoLeer])
def listar_empleados_endpoint(especialidad: str | None = Query(None), estado: EstadoEmpleado | None = Query(None), sesion: Session = Depends(obtener_sesion)):
    return crud.listar_empleados(sesion, especialidad, estado.value if estado else None)

@app.get("/empleados/{empleado_id}", response_model=EmpleadoLeer)
def obtener_empleado_endpoint(empleado_id: int, sesion: Session = Depends(obtener_sesion)):
    return crud.obtener_empleado(sesion, empleado_id)

@app.put("/empleados/{empleado_id}", response_model=EmpleadoLeer)
def actualizar_empleado_endpoint(empleado_id: int, payload: EmpleadoCrear, sesion: Session = Depends(obtener_sesion)):
    return crud.actualizar_empleado(sesion, empleado_id, payload.dict())

@app.delete("/empleados/{empleado_id}")
def eliminar_empleado_endpoint(empleado_id: int, sesion: Session = Depends(obtener_sesion)):
    return crud.eliminar_empleado(sesion, empleado_id)
