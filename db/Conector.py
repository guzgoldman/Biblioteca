import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cargar variables de entorno
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

# URL de conexión
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DATABASE_URL,
    echo=False,          # pon True si querés ver todas las queries en consola
    pool_pre_ping=True,  # evita conexiones muertas
)

# Base global compartida por todos los modelos
Base = declarative_base()
Base.metadata.bind = engine   # 🔥 ENLAZADO DIRECTO

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

class Conector:
    @staticmethod
    def get_session():
        """Devuelve una nueva sesión SQLAlchemy correctamente enlazada."""
        return SessionLocal()