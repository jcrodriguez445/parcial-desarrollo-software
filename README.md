#  Sistema de Gestión de Proyectos - FastAPI

Este proyecto es una **API ** desarrollada con **FastAPI** y **SQLModel** que permite gestionar **empleados** y **proyectos**, manteniendo relaciones entre ambos.  
Incluye operaciones CRUD completas, validaciones, manejo de errores, y documentación automática con Swagger UI y Redoc.

---

##  Características Principales

- Creación, lectura, actualización y eliminación (CRUD) de **empleados** y **proyectos**.  
- Relación entre empleados y proyectos.  
- Reasignación de gerente a un proyecto.  
- Registro histórico de eliminaciones.  
- Uso de **SQLModel** (SQLAlchemy + Pydantic).  
- Manejo de errores HTTP (400, 404, 422, etc.).  
- Documentación interactiva en `/docs` 

---

##  Estructura del Proyecto

```
project-management/
│
├── app/
│   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── modelos.py
│
├── app.db
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── .venv/
```

---

##  Instalación y Configuración

### 1 Clonar el repositorio

```bash
git clone https://github.com/tuusuario/project-management.git
cd project-management
```

### 2 Crear un entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate  
.venv\Scripts\activate    
```

### 3 Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4 Ejecutar el servidor

```bash
uvicorn app.main:app --reload
```

### 5 Acceder a la documentación

- 👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- 👉 [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Modelos de Datos

###  Empleado
| Campo | Tipo | Descripción |
|-------|------|--------------|
| id | int | Identificador único |
| nombre | str | Nombre completo del empleado |
| puesto | str | Cargo o rol dentro de la empresa |
| proyectos | list | Lista de proyectos asignados |

### Proyecto
| Campo | Tipo | Descripción |
|-------|------|--------------|
| id | int | Identificador único |
| nombre | str | Nombre del proyecto |
| descripcion | str | Descripción del proyecto |
| gerente_id | int | ID del empleado gerente |
| empleados | list | Empleados asignados al proyecto |

---

## Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|-----------|-------------|
| **GET** | `/empleados/` | Obtener todos los empleados |
| **POST** | `/empleados/` | Crear un nuevo empleado |
| **GET** | `/empleados/{id}` | Obtener un empleado por ID |
| **DELETE** | `/empleados/{id}` | Eliminar un empleado |
| **GET** | `/proyectos/` | Obtener todos los proyectos |
| **POST** | `/proyectos/` | Crear un nuevo proyecto |
| **GET** | `/proyectos/{id}` | Obtener un proyecto por ID |
| **PUT** | `/proyectos/{id}` | Actualizar un proyecto existente |
| **PATCH** | `/proyectos/{id}/reasignar-gerente` | Reasignar gerente de un proyecto |
| **DELETE** | `/proyectos/{id}` | Eliminar un proyecto |

---

##  Ejemplos de Uso

### Crear un empleado

```bash
POST /empleados/
{
  "nombre": "Carlos Gómez",
  "puesto": "Desarrollador Backend"
}
```

### Crear un proyecto

```bash
POST /proyectos/
{
  "nombre": "Sistema Interno",
  "descripcion": "Aplicación interna de gestión",
  "gerente_id": 1
}
```

### Reasignar gerente

```bash
PATCH /proyectos/1/reasignar-gerente

{
  "nuevo_gerente_id": 2
}
```

### Actualizar un proyecto

```bash
PUT /proyectos/1

{
  "nombre": "Sistema Interno V2",
  "descripcion": "Versión actualizada con nuevas funciones",
  "gerente_id": 2
}
```

---

##  Manejo de Errores

| Código | Descripción |
|--------|--------------|
| **200 OK** | Solicitud exitosa |
| **201 Created** | Recurso creado correctamente |
| **202 Accepted** | Solicitud aceptada para procesamiento |
| **204 No Content** | Solicitud exitosa sin contenido |
| **400 Bad Request** | Datos inválidos |
| **404 Not Found** | Recurso no encontrado |
| **422 Unprocessable Entity** | Error en validación de datos |

---

##  Tecnologías Usadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [SQLite](https://www.sqlite.org/)
- [Uvicorn](https://www.uvicorn.org/)
- [Pydantic](https://docs.pydantic.dev/)

---

##  Autor

**Nombre:** *Juan Carlos Rodriguez Sanchez*  
**Proyecto - Gestión de Proyectos con FastAPI*  


---


