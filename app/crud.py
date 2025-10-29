from sqlmodel import select, Session
from fastapi import HTTPException, status
from app.modelos import Empleado, Proyecto, VínculoProyectoEmpleado

# ----- EMPLEADOS -----

def crear_empleado(sesion: Session, empleado: Empleado):
    sesion.add(empleado)
    sesion.commit()
    sesion.refresh(empleado)
    return empleado

def listar_empleados(sesion: Session, especialidad: str | None = None, estado: str | None = None):
    q = select(Empleado)
    if especialidad:
        q = q.where(Empleado.especialidad == especialidad)
    if estado:
        q = q.where(Empleado.estado == estado)
    return sesion.exec(q).all()

def obtener_empleado(sesion: Session, empleado_id: int):
    emp = sesion.get(Empleado, empleado_id)
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empleado no encontrado")
    return emp
