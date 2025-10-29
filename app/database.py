from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

def inicializar_bd():
    # importamos modelos aquí para evitar import circular
    from app.modelos import Empleado, Proyecto, VínculoProyectoEmpleado, HistorialEmpleadoEliminado, HistorialProyectoEliminado
    SQLModel.metadata.create_all(engine)

def obtener_sesion():
    with Session(engine) as sesion:
        yield sesion
