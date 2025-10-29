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

def actualizar_empleado(sesion: Session, empleado_id: int, datos: dict):
    emp = obtener_empleado(sesion, empleado_id)
    for k, v in datos.items():
        setattr(emp, k, v)
    sesion.add(emp)
    sesion.commit()
    sesion.refresh(emp)
    return emp

def eliminar_empleado(sesion: Session, empleado_id: int):
    from app.modelos import HistorialEmpleadoEliminado
    emp = obtener_empleado(sesion, empleado_id)

    proyectos_gerenciados = sesion.exec(select(Proyecto).where(Proyecto.gerente_id == emp.id)).all()
    if proyectos_gerenciados:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Empleado es gerente de uno o más proyectos y no puede eliminarse")

    # Registrar en historial antes de eliminar
    historial = HistorialEmpleadoEliminado(
        nombre=emp.nombre,
        especialidad=emp.especialidad,
        salario=emp.salario,
        estado=emp.estado.value
    )
    sesion.add(historial)

    # Eliminar vínculos
    vínculos = sesion.exec(select(VínculoProyectoEmpleado).where(VínculoProyectoEmpleado.empleado_id == emp.id)).all()
    for v in vínculos:
        sesion.delete(v)

    sesion.delete(emp)
    sesion.commit()
    return {"ok": True, "mensaje": "Empleado eliminado y registrado en historial"}

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

# ----- ASIGNACIONES -----

def asignar_empleado(sesion: Session, proyecto_id: int, empleado_id: int):
    obtener_proyecto(sesion, proyecto_id)
    emp = sesion.get(Empleado, empleado_id)
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empleado no encontrado")
    existe = sesion.exec(select(VínculoProyectoEmpleado).where(
        (VínculoProyectoEmpleado.proyecto_id == proyecto_id) & (VínculoProyectoEmpleado.empleado_id == empleado_id)
    )).first()
    if existe:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Empleado ya asignado al proyecto")
    enlace = VínculoProyectoEmpleado(proyecto_id=proyecto_id, empleado_id=empleado_id)
    sesion.add(enlace)
    sesion.commit()
    return {"ok": True}

def desasignar_empleado(sesion: Session, proyecto_id: int, empleado_id: int):
    enlace = sesion.exec(select(VínculoProyectoEmpleado).where(
        (VínculoProyectoEmpleado.proyecto_id == proyecto_id) & (VínculoProyectoEmpleado.empleado_id == empleado_id)
    )).first()
    if not enlace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asignación no encontrada")
    sesion.delete(enlace)
    sesion.commit()
    return {"ok": True}

def proyectos_de_empleado(sesion: Session, empleado_id: int):
    emp = obtener_empleado(sesion, empleado_id)
    return emp.proyectos

def empleados_de_proyecto(sesion: Session, proyecto_id: int):
    proj = obtener_proyecto(sesion, proyecto_id)
    return proj.empleados
    