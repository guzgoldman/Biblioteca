"""
Script para diagnosticar y arreglar problemas con administradores.
"""
import sys
from pathlib import Path
import hashlib

# Agregar el directorio padre al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from db.Conector import SessionLocal
from modelo.Administrador import Administrador


def listar_administradores_detalle():
    """Lista todos los administradores con detalles de sus contraseñas."""
    session = SessionLocal()
    
    try:
        admins = session.query(Administrador).all()
        
        if not admins:
            print("ℹ️  No hay administradores registrados en el sistema.")
            return
        
        print(f"\n👥 Administradores registrados ({len(admins)}):")
        print("-" * 80)
        for admin in admins:
            print(f"ID: {admin.id}")
            print(f"DNI: {admin.dni}")
            print(f"Nombre: {admin.nombre} {admin.apellido}")
            print(f"Password (primeros 20 chars): {admin.password[:20]}...")
            print(f"¿Es hash SHA-256? {len(admin.password) == 64 and all(c in '0123456789abcdef' for c in admin.password.lower())}")
            print("-" * 80)
        
    except Exception as e:
        print(f"❌ Error al listar administradores: {e}")
    finally:
        session.close()


def actualizar_password_administrador(dni: str, nueva_password: str):
    """Actualiza la contraseña de un administrador existente, hasheándola correctamente."""
    session = SessionLocal()
    
    try:
        # Buscar administrador
        admin = session.query(Administrador).filter_by(dni=dni).first()
        
        if not admin:
            print(f"❌ No se encontró administrador con DNI: {dni}")
            return False
        
        # Hashear la nueva contraseña
        password_hash = hashlib.sha256(nueva_password.encode('utf-8')).hexdigest()
        
        print(f"📝 Actualizando contraseña para {admin.nombre} {admin.apellido}")
        print(f"   Password original: {nueva_password}")
        print(f"   Password hash: {password_hash}")
        
        # Actualizar contraseña
        admin.password = password_hash
        session.commit()
        
        print("✅ Contraseña actualizada exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error al actualizar contraseña: {e}")
        session.rollback()
        return False
    finally:
        session.close()


def crear_admin_nuevo(dni: str, nombre: str, apellido: str, password: str):
    """Crea un nuevo administrador asegurándonos que la contraseña se hashee."""
    session = SessionLocal()
    
    try:
        # Verificar si ya existe
        admin_existente = session.query(Administrador).filter_by(dni=dni).first()
        
        if admin_existente:
            print(f"⚠️  Ya existe un administrador con DNI {dni}")
            respuesta = input("¿Quieres actualizar su contraseña? (s/n): ")
            if respuesta.lower() in ['s', 'si', 'sí', 'y', 'yes']:
                return actualizar_password_administrador(dni, password)
            return False
        
        # Hashear contraseña manualmente para estar seguros
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        print(f"📝 Creando nuevo administrador:")
        print(f"   DNI: {dni}")
        print(f"   Nombre: {nombre} {apellido}")
        print(f"   Password original: {password}")
        print(f"   Password hash: {password_hash}")
        
        # Crear administrador directamente (sin usar el método crear)
        admin = Administrador(
            dni=dni,
            nombre=nombre,
            apellido=apellido,
            password=password_hash
        )
        
        session.add(admin)
        session.commit()
        session.refresh(admin)
        
        print("✅ Administrador creado exitosamente!")
        print(f"   ID: {admin.id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al crear administrador: {e}")
        session.rollback()
        return False
    finally:
        session.close()


def main():
    print("=" * 80)
    print("   DIAGNÓSTICO Y REPARACIÓN DE ADMINISTRADORES")
    print("=" * 80)
    
    try:
        # Mostrar estado actual
        listar_administradores_detalle()
        
        print("\n🔧 Opciones:")
        print("1. Crear administrador de prueba")
        print("2. Actualizar contraseña de administrador existente")
        print("3. Solo mostrar información")
        
        opcion = input("\nSelecciona una opción (1-3): ").strip()
        
        if opcion == "1":
            print("\n📝 Creando administrador de prueba...")
            crear_admin_nuevo("12345678", "Admin", "Sistema", "admin123")
            print("\n📄 Estado después de la creación:")
            listar_administradores_detalle()
            
        elif opcion == "2":
            dni = input("DNI del administrador: ").strip()
            password = input("Nueva contraseña: ").strip()
            if dni and password:
                actualizar_password_administrador(dni, password)
                print("\n📄 Estado después de la actualización:")
                listar_administradores_detalle()
            else:
                print("❌ DNI y contraseña son obligatorios")
                
        print("\n🎯 Credenciales para login:")
        print("   Si creaste el admin de prueba:")
        print("   DNI: 12345678")
        print("   Contraseña: admin123")
        
    except Exception as e:
        print(f"\n❌ Error de conexión: {e}")


if __name__ == "__main__":
    main()