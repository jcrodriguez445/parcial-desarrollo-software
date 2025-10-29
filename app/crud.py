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

# ----- PROYECTOS -----

def crear_proyecto(sesion: Session, proyecto: Proyecto):
    existe = sesion.exec(select(Proyecto).where(Proyecto.nombre == proyecto.nombre)).first()
    if existe:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Nombre de proyecto ya existe")
    gerente = sesion.get(Empleado, proyecto.gerente_id)
    if not gerente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gerente no encontrado")
    sesion.add(proyecto)
    sesion.commit()
    sesion.refresh(proyecto)
    return proyecto

def listar_proyectos(sesion: Session, estado: str | None = None, presupuesto_min: float | None = None):
    q = select(Proyecto)
    if estado:
        q = q.where(Proyecto.estado == estado)
    if presupuesto_min is not None:
        q = q.where(Proyecto.presupuesto >= presupuesto_min)
    return sesion.exec(q).all()

def obtener_proyecto(sesion: Session, proyecto_id: int):
    proj = sesion.get(Proyecto, proyecto_id)
    if not proj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")
    return proj

def eliminar_proyecto(sesion: Session, proyecto_id: int, cascada: bool = False):
    from app.modelos import HistorialProyectoEliminado
    proj = obtener_proyecto(sesion, proyecto_id)

    vínculos = sesion.exec(select(VínculoProyectoEmpleado).where(VínculoProyectoEmpleado.proyecto_id == proj.id)).all()
    if vínculos and not cascada:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Proyecto tiene empleados asignados. Use cascada para eliminar")

    # Guardar en historial antes de eliminar
    historial = HistorialProyectoEliminado(
        nombre=proj.nombre,
        descripcion=proj.descripcion,
        presupuesto=proj.presupuesto,
        estado=proj.estado.value,
        gerente_id=proj.gerente_id
    )
    sesion.add(historial)

    for v in vínculos:
        sesion.delete(v)

    sesion.delete(proj)
    sesion.commit()
    return {"ok": True, "mensaje": "Proyecto eliminado y registrado en historial"}
