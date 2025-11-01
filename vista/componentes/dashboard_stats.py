from datetime import datetime

class DashboardStats:
    """Clase para obtener estadísticas del sistema de biblioteca."""

    @staticmethod
    def _get_session(external_session=None):
        """Devuelve la sesión activa o crea una nueva si no se pasó ninguna."""
        if external_session is not None:
            return external_session, False  # False = no cerrar al final
        from db.Conector import SessionLocal
        return SessionLocal(), True  # True = cerrar al final

    @staticmethod
    def obtener_total_socios(session=None) -> int:
        from modelo.Socio import Socio
        from sqlalchemy import func
        s, close_after = DashboardStats._get_session(session)
        try:
            total = s.query(func.count(Socio.id)).scalar() or 0
            return total
        finally:
            if close_after:
                s.close()

    @staticmethod
    def obtener_total_libros(session=None) -> int:
        from modelo.Libro import Libro
        from sqlalchemy import func
        s, close_after = DashboardStats._get_session(session)
        try:
            return s.query(func.count(Libro.id)).scalar() or 0
        finally:
            if close_after:
                s.close()

    @staticmethod
    def obtener_prestamos_emitidos(session=None) -> int:
        from modelo.Prestamo import Prestamo
        from sqlalchemy import func
        s, close_after = DashboardStats._get_session(session)
        try:
            return s.query(func.count(Prestamo.id)).scalar() or 0
        finally:
            if close_after:
                s.close()

    @staticmethod
    def obtener_prestamos_activos(session=None) -> int:
        from modelo.Prestamo import Prestamo
        from sqlalchemy import func
        s, close_after = DashboardStats._get_session(session)
        try:
            return s.query(func.count(Prestamo.id)).filter(Prestamo.fecha_devolucion == None).scalar() or 0
        finally:
            if close_after:
                s.close()

    @staticmethod
    def obtener_fecha_actual() -> str:
        """Devuelve la fecha actual formateada."""
        return datetime.now().strftime('%d/%m/%Y %H:%M')