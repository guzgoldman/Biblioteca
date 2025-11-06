# dashboard_stats.py

from datetime import datetime
from db.session_manager import SessionManager

class DashboardStats:
    """Clase para obtener estadísticas del sistema de biblioteca."""

    @staticmethod
    def _get_session(external_session=None):
        """Devuelve la sesión activa o crea una nueva si no se pasó ninguna."""
        if external_session is not None:
            return external_session, False
        return SessionManager.get_session(), False  # 🔹 nunca se cierra desde aquí

    @staticmethod
    def obtener_total_socios(session=None) -> int:
        from modelo.Socio import Socio
        from sqlalchemy import func
        s, _ = DashboardStats._get_session(session)
        return s.query(func.count(Socio.id)).scalar() or 0

    @staticmethod
    def obtener_total_libros(session=None) -> int:
        from modelo.Libro import Libro
        from sqlalchemy import func
        s, _ = DashboardStats._get_session(session)
        return s.query(func.count(Libro.id)).scalar() or 0

    @staticmethod
    def obtener_prestamos_emitidos(session=None) -> int:
        from modelo.Prestamo import Prestamo
        from sqlalchemy import func
        s, _ = DashboardStats._get_session(session)
        return s.query(func.count(Prestamo.id)).scalar() or 0

    @staticmethod
    def obtener_prestamos_activos(session=None) -> int:
        from modelo.Prestamo import Prestamo
        from sqlalchemy import func
        s, _ = DashboardStats._get_session(session)
        return s.query(func.count(Prestamo.id)).filter(Prestamo.fecha_devolucion == None).scalar() or 0

    @staticmethod
    def obtener_fecha_actual() -> str:
        """Devuelve la fecha actual formateada."""
        return datetime.now().strftime('%d/%m/%Y %H:%M')