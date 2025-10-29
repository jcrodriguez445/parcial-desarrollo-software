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

# ----- PROYECTOS -----

@app.post("/proyectos", response_model=ProyectoLeer, status_code=201)
def crear_proyecto_endpoint(proyecto: ProyectoCrear, sesion: Session = Depends(obtener_sesion)):
    nuevo = Proyecto.from_orm(proyecto)
    return crud.crear_proyecto(sesion, nuevo)

@app.get("/proyectos", response_model=List[ProyectoLeer])
def listar_proyectos_endpoint(estado: EstadoProyecto | None = Query(None), presupuesto_min: float | None = Query(None), sesion: Session = Depends(obtener_sesion)):
    return crud.listar_proyectos(sesion, estado.value if estado else None, presupuesto_min)

@app.get("/proyectos/{proyecto_id}", response_model=ProyectoLeer)
def obtener_proyecto_endpoint(proyecto_id: int, sesion: Session = Depends(obtener_sesion)):
    return crud.obtener_proyecto(sesion, proyecto_id)

@app.delete("/proyectos/{proyecto_id}")
def eliminar_proyecto_endpoint(proyecto_id: int, cascada: bool | None = Query(False), sesion: Session = Depends(obtener_sesion)):
    return crud.eliminar_proyecto(sesion, proyecto_id, cascada=cascada)

# ----- ASIGNACIONES -----

@app.post("/proyectos/{proyecto_id}/asignar/{empleado_id}")
def asignar_empleado_endpoint(proyecto_id: int, empleado_id: int, sesion: Session = Depends(obtener_sesion)):
    return crud.asignar_empleado(sesion, proyecto_id, empleado_id)

@app.post("/proyectos/{proyecto_id}/desasignar/{empleado_id}")
def desasignar_empleado_endpoint(proyecto_id: int, empleado_id: int, sesion: Session = Depends(obtener_sesion)):
    return crud.desasignar_empleado(sesion, proyecto_id, empleado_id)

# ----- CONSULTAS RELACIONALES -----

@app.get("/empleados/{empleado_id}/proyectos", response_model=List[ProyectoLeer])
def proyectos_del_empleado_endpoint(empleado_id: int, sesion: Session = Depends(obtener_sesion)):
    return crud.proyectos_de_empleado(sesion, empleado_id)

@app.get("/proyectos/{proyecto_id}/empleados", response_model=List[EmpleadoLeer])
def empleados_del_proyecto_endpoint(proyecto_id: int, sesion: Session = Depends(obtener_sesion)):
    return crud.empleados_de_proyecto(sesion, proyecto_id)