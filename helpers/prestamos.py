from sqlalchemy import select
from sqlalchemy.orm import Session
from db.Conector import SessionLocal
from modelo import Prestamo, Socio, Ejemplar, Administrador

def prestar_por_dni_y_codigo(session: Session, dni: str, codigo_ejemplar: str) -> Prestamo:
    """Crea un préstamo para el ejemplar (por código) a un usuario (por DNI)."""
    dni = (dni or "").strip()
    codigo_ejemplar = (codigo_ejemplar or "").strip()

    if not dni or not codigo_ejemplar:
        raise ValueError("DNI y código de ejemplar son obligatorios")

    socio = session.execute(select(Socio).where(Socio.dni == dni)).scalar_one_or_none()
    if not socio:
        raise ValueError(f"Socio con DNI {dni} no existe")

    ejemplar = session.execute(select(Ejemplar).where(Ejemplar.codigo == codigo_ejemplar)).scalar_one_or_none()
    if not ejemplar:
        raise ValueError(f"Ejemplar con código {codigo_ejemplar} no existe")

    session.execute(select(Ejemplar).where(Ejemplar.id == ejemplar.id).with_for_update())

    prestamo_activo = session.execute(
        select(Prestamo).where(Prestamo.ejemplar_id == ejemplar.id, Prestamo.fecha_devolucion.is_(None))
    ).scalar_one_or_none()
    if prestamo_activo:
        raise ValueError("Ya existe un préstamo activo para ese ejemplar")

    prestamo = Prestamo.crear(session, ejemplar, socio)
    return prestamo


def devolver_por_id(session: Session, id_prestamo: int) -> Prestamo:
    """Devuelve un préstamo por id y libera el ejemplar."""
    prestamo = session.get(Prestamo, id_prestamo)
    if not prestamo:
        raise ValueError("Préstamo no encontrado")

    prestamo.devolver(session)
    return prestamo
