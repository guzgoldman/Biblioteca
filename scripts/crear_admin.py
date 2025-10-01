"""
Script para crear administradores en el sistema.
Ejecutar este script para agregar un administrador de prueba.
"""
import sys
from pathlib import Path

# Agregar el directorio padre al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from db.Conector import SessionLocal
from modelo.Administrador import Administrador


def crear_admin_prueba():
    """Crea un administrador de prueba para el sistema."""
    session = SessionLocal()
    
    try:
        # Verificar si ya existe
        admin_existente = session.query(Administrador).filter_by(dni="12345678").first()
        
        if admin_existente:
            print("✅ Ya existe un administrador con DNI 12345678")
            print(f"   Nombre: {admin_existente.nombre} {admin_existente.apellido}")
            return
        
        # Crear nuevo administrador
        admin = Administrador.crear(
            session=session,
            dni="12345678",
            nombre="Admin",
            apellido="Sistema",
            password="admin123",  # La contraseña será hasheada automáticamente
            commit=True
        )
        
        print("✅ Administrador creado exitosamente!")
        print(f"   DNI: {admin.dni}")
        print(f"   Nombre: {admin.nombre} {admin.apellido}")
        print(f"   Contraseña: admin123")
        print("\n📝 Usa estas credenciales para iniciar sesión:")
        print(f"   DNI: 12345678")
        print(f"   Contraseña: admin123")
        
    except Exception as e:
        print(f"❌ Error al crear administrador: {e}")
        session.rollback()
    finally:
        session.close()


def listar_administradores():
    """Lista todos los administradores del sistema."""
    session = SessionLocal()
    
    try:
        admins = session.query(Administrador).all()
        
        if not admins:
            print("ℹ️  No hay administradores registrados en el sistema.")
            return
        
        print(f"\n👥 Administradores registrados ({len(admins)}):")
        print("-" * 60)
        for admin in admins:
            print(f"ID: {admin.id} | DNI: {admin.dni} | {admin.nombre} {admin.apellido}")
        print("-" * 60)
        
    except Exception as e:
        print(f"❌ Error al listar administradores: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    print("=" * 60)
    print("   GESTIÓN DE ADMINISTRADORES - Sistema de Biblioteca")
    print("=" * 60)
    
    try:
        listar_administradores()
        print()
        crear_admin_prueba()
        print()
        listar_administradores()
    except Exception as e:
        print(f"\n❌ Error de conexión con la base de datos: {e}")
        print("\nAsegúrate de que:")
        print("1. El servidor MySQL esté ejecutándose")
        print("2. Las credenciales en .env sean correctas")
        print("3. La base de datos y las tablas estén creadas")
