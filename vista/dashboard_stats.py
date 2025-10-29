"""
Módulo para obtener estadísticas del dashboard desde la base de datos.
"""
import sys
from pathlib import Path

# Agregar el directorio padre al path para poder importar los módulos
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime


class DashboardStats:
    """Clase para obtener estadísticas del sistema de biblioteca."""
    
    @staticmethod
    def _get_session_and_models():
        """Obtiene una sesión de base de datos y los modelos. Lazy import."""
        try:
            from db.Conector import SessionLocal
            from modelo.Libro import Libro
            from modelo.Socio import Socio
            from modelo.Prestamo import Prestamo
            from modelo.Ejemplar import Ejemplar
            from sqlalchemy import func
            
            session = SessionLocal()
            return session, Libro, Socio, Prestamo, Ejemplar, func
        except Exception as e:
            print(f"Error al conectar con la base de datos: {e}")
            return None, None, None, None, None, None
    
    @staticmethod
    def obtener_total_libros() -> int:
        """Obtiene el total de libros registrados en el sistema."""
        session, Libro, _, _, _, func = DashboardStats._get_session_and_models()
        if session is None or Libro is None:
            return 0
        
        try:
            total = session.query(func.count(Libro.id)).scalar()
            return total or 0
        except Exception as e:
            print(f"Error al obtener total de libros: {e}")
            return 0
        finally:
            session.close()
    
    @staticmethod
    def obtener_total_ejemplares() -> int:
        """Obtiene el total de ejemplares en el sistema."""
        session, _, _, _, Ejemplar, func = DashboardStats._get_session_and_models()
        if session is None or Ejemplar is None:
            return 0
        
        try:
            total = session.query(func.count(Ejemplar.id)).scalar()
            return total or 0
        except Exception as e:
            print(f"Error al obtener total de ejemplares: {e}")
            return 0
        finally:
            session.close()
    
    @staticmethod
    def obtener_total_socios() -> int:
        """Obtiene el total de socios registrados."""
        session, _, Socio, _, _, func = DashboardStats._get_session_and_models()
        if session is None or Socio is None:
            return 0
        
        try:
            total = session.query(func.count(Socio.id)).scalar()
            return total or 0
        except Exception as e:
            print(f"Error al obtener total de socios: {e}")
            return 0
        finally:
            session.close()
    
    @staticmethod
    def obtener_prestamos_emitidos() -> int:
        """Obtiene el total de préstamos emitidos (histórico completo)."""
        session, _, _, Prestamo, _, func = DashboardStats._get_session_and_models()
        if session is None or Prestamo is None:
            return 0
        
        try:
            total = session.query(func.count(Prestamo.id)).scalar()
            return total or 0
        except Exception as e:
            print(f"Error al obtener préstamos emitidos: {e}")
            return 0
        finally:
            session.close()
    
    @staticmethod
    def obtener_prestamos_activos() -> int:
        """Obtiene el total de préstamos activos (no devueltos)."""
        session, _, _, Prestamo, _, func = DashboardStats._get_session_and_models()
        if session is None or Prestamo is None:
            return 0
        
        try:
            total = session.query(func.count(Prestamo.id)).filter(
                Prestamo.fecha_devolucion == None
            ).scalar()
            return total or 0
        except Exception as e:
            print(f"Error al obtener préstamos activos: {e}")
            return 0
        finally:
            session.close()
    
    @staticmethod
    def obtener_prestamos_devueltos() -> int:
        """Obtiene el total de préstamos devueltos."""
        session, _, _, Prestamo, _, func = DashboardStats._get_session_and_models()
        if session is None or Prestamo is None:
            return 0
        
        try:
            total = session.query(func.count(Prestamo.id)).filter(
                Prestamo.fecha_devolucion != None
            ).scalar()
            return total or 0
        except Exception as e:
            print(f"Error al obtener préstamos devueltos: {e}")
            return 0
        finally:
            session.close()
    
    @staticmethod
    def obtener_prestamos_vencidos() -> int:
        """Obtiene el total de préstamos vencidos (no devueltos y fecha pasada)."""
        session, _, _, Prestamo, _, func = DashboardStats._get_session_and_models()
        if session is None or Prestamo is None:
            return 0
        
        try:
            ahora = datetime.now()
            total = session.query(func.count(Prestamo.id)).filter(
                Prestamo.fecha_devolucion == None,
                Prestamo.fecha_devolucion_pactada < ahora
            ).scalar()
            return total or 0
        except Exception as e:
            print(f"Error al obtener préstamos vencidos: {e}")
            return 0
        finally:
            session.close()
    
    @staticmethod
    def obtener_fecha_actual() -> str:
        """Obtiene la fecha actual formateada."""
        return datetime.now().strftime('%d/%m/%Y %H:%M')
    
    @staticmethod
    def obtener_todas_estadisticas() -> dict:
        """Obtiene todas las estadísticas del dashboard en un solo llamado."""
        session, Libro, Socio, Prestamo, Ejemplar, func = DashboardStats._get_session_and_models()
        
        # Si no hay conexión, devolver valores por defecto
        if session is None:
            return {
                'total_libros': 0,
                'total_ejemplares': 0,
                'total_socios': 0,
                'prestamos_emitidos': 0,
                'prestamos_activos': 0,
                'prestamos_devueltos': 0,
                'prestamos_vencidos': 0,
                'fecha_actual': DashboardStats.obtener_fecha_actual()
            }
        
        try:
            ahora = datetime.now()
            stats = {
                'total_libros': session.query(func.count(Libro.id)).scalar() or 0,
                'total_ejemplares': session.query(func.count(Ejemplar.id)).scalar() or 0,
                'total_socios': session.query(func.count(Socio.id)).scalar() or 0,
                'prestamos_emitidos': session.query(func.count(Prestamo.id)).scalar() or 0,
                'prestamos_activos': session.query(func.count(Prestamo.id)).filter(
                    Prestamo.fecha_devolucion == None
                ).scalar() or 0,
                'prestamos_devueltos': session.query(func.count(Prestamo.id)).filter(
                    Prestamo.fecha_devolucion != None
                ).scalar() or 0,
                'prestamos_vencidos': session.query(func.count(Prestamo.id)).filter(
                    Prestamo.fecha_devolucion == None,
                    Prestamo.fecha_devolucion_pactada < ahora
                ).scalar() or 0,
                'fecha_actual': DashboardStats.obtener_fecha_actual()
            }
            return stats
        except Exception as e:
            print(f"Error al obtener estadísticas: {e}")
            return {
                'total_libros': 0,
                'total_ejemplares': 0,
                'total_socios': 0,
                'prestamos_emitidos': 0,
                'prestamos_activos': 0,
                'prestamos_devueltos': 0,
                'prestamos_vencidos': 0,
                'fecha_actual': DashboardStats.obtener_fecha_actual()
            }
        finally:
            session.close()
