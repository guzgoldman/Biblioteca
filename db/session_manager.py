# db/session_manager.py

class SessionManager:
    """Manejador global de sesión SQLAlchemy."""
    _session = None

    @classmethod
    def get_session(cls):
        """Devuelve la sesión activa o crea una nueva si fue cerrada o inválida."""
        try:
            if cls._session and cls._session.is_active:
                return cls._session
        except Exception:
            pass

        # 🔹 Import diferido aquí, evita el bucle de importaciones
        from db.Conector import SessionLocal
        cls._session = SessionLocal()
        return cls._session

    @classmethod
    def close_session(cls):
        if cls._session:
            try:
                cls._session.close()
            except Exception:
                pass
            cls._session = None

    @classmethod
    def reset_session(cls):
        cls.close_session()
        from db.Conector import SessionLocal
        cls._session = SessionLocal()
        return cls._session